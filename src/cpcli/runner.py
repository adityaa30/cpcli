import json
import logging
import os
import shutil
from http.client import HTTPSConnection
from subprocess import Popen, PIPE
from typing import Optional, List, Dict

from lxml.html import document_fromstring

from cpcli.platforms import Platforms
from cpcli.question import Question
from cpcli.utils.config import CpCliConfig

logger = logging.getLogger()


class Runner:
    def __init__(self, platform: str, contest: str, template: str, config: CpCliConfig) -> None:
        self.platform = platform
        self.contest = contest

        self.config = config
        self.base_dir = Platforms.get_dir_path(self.config.contest_files_dir, platform, contest)
        self.metadata_path = os.path.join(self.base_dir, '.metadata.json')

        self.template = template

        self.questions: List[Question] = []

        if not os.path.exists(self.base_dir):
            logger.debug(f'Creating base directory: {self.base_dir}')
            os.makedirs(self.base_dir)

    def to_dict(self) -> Dict:
        metadata: Dict = {
            'platform': self.platform,
            'contest': self.contest,
            'base_dir': self.base_dir,
            'template': self.template,
            'questions': []
        }
        for question in self.questions:
            metadata['questions'].append(question.to_dict())

        return metadata

    @property
    def metadata(self):
        return self.to_dict()

    def get_question(self, val: str) -> Optional[Question]:
        val = val.lower()
        for idx, question in enumerate(self.questions, start=1):
            if str(idx) == val or val in question.title.lower():
                return question
        return None

    def show_all_questions(self, verbose: bool = False) -> None:
        for question in self.questions:
            logging.info(question)
            if verbose:
                for test in question.test_cases:
                    logging.info(test)

    def run_test_cases(self, val: str, file: Optional[str] = None) -> None:
        question = self.get_question(val)

        if not question:
            logger.warning('Invalid question entered. Following are available:')
            for question in self.questions:
                logger.warning(f"[{question.idx}]\t{question.title}")
            return

        if file and not os.path.exists(file):
            logger.warning(f'"{file}" solution file do not exist')
            return

        logger.info(f'Checking question: {question.title}')

        # Store the executable file in question's directory
        compiled_executable = os.path.join(self.base_dir, 'program')

        compiled_args = [
            'g++', question.path,
            '-o', compiled_executable,
            # Add extra flags below 🛸🐙
            '-DLOCAL',
            #  '-Wall', '-Wextra',
            # '-pedantic', '-std=c++11', '-O2',
            # '-Wshadow', '-Wformat=2', '-Wfloat-equal',
            # '-Wconversion', '-Wlogical-op', '-Wshift-overflow=2',
            # '-Wduplicated-cond', '-Wcast-qual', '-Wcast-align',
            # '-D_GLIBCXX_DEBUG', '-D_GLIBCXX_DEBUG_PEDANTIC',
            # '-D_FORTIFY_SOURCE=2', '-fsanitize=address',
            # '-fsanitize=undefined', '-fno-sanitize-recover',
            # '-fstack-protector'
        ]

        compile_process = Popen(compiled_args, stdout=PIPE)
        compile_process.wait()

        for test_case in question.test_cases:
            test_case.execute(compiled_executable)

        os.remove(compiled_executable)

    def load_questions(self, force_download=False) -> None:
        if force_download or (not os.path.exists(self.metadata_path)):
            if self.platform == 'cf':
                self.questions = self.get_questions_codeforces()
            elif self.platform == 'cc':
                self.questions = self.get_questions_codechef()
            self.save_questions()
            return

        self.questions = []
        with open(self.metadata_path, 'r') as file:
            metadata = json.load(file)

        for question in metadata['questions']:
            self.questions.append(Question.from_dict(question))

    def get_questions_codeforces(self) -> List[Question]:
        logger.info(f'Downloading page https://codeforces.com/contest/{self.contest}/problems')

        url = 'codeforces.com'
        conn = HTTPSConnection(url)
        conn.request("GET", f"/contest/{self.contest}/problems")
        response = conn.getresponse()

        if response.getcode() != 200:
            err = Exception(f'No contest found for codeforces/{self.contest} ❌❌')
            conn.close()
            raise err

        html = response.read().decode()
        conn.close()
        questions: List[Question] = []

        doc = document_fromstring(html)
        caption = doc.xpath('//div[@class="caption"]/text()')[0]

        logger.info(f'Found: {caption} ✅')
        logger.info('Scraping problems:')

        problems = doc.xpath('//div[@class="problem-statement"]')
        for idx, problem in enumerate(problems):
            title = problem.find_class("title")[0].text_content()
            time_limit = problem.find_class("time-limit")[0].text_content()

            time_limit = time_limit[len('time limit per test'):].split(' ')[0]
            try:
                question = Question(idx, title, self.base_dir, float(time_limit))
            except ValueError:
                question = Question(idx, title, self.base_dir, 5.0)

            sample_tests = problem.find_class("sample-test")[0]
            inputs = sample_tests.find_class('input')
            outputs = sample_tests.find_class('output')

            for inp, out in zip(inputs, outputs):
                sample_input = inp.xpath('descendant-or-self::pre/text()')[0]
                sample_output = out.xpath('descendant-or-self::pre/text()')[0]
                question.add_test(sample_input, sample_output)

            questions.append(question)
            logger.info(question)

        return questions

    def save_questions(self) -> None:
        if len(self.questions) == 0:
            return

        for question in self.questions:
            # Copy the template
            template_named_file = os.path.join(self.base_dir, os.path.basename(self.template))
            if not os.path.exists(question.path):
                shutil.copy(self.template, self.base_dir)
                os.rename(template_named_file, question.path)

        # Save/Update the metadata
        with open(self.metadata_path, 'w') as file:
            json.dump(self.metadata, file, indent=2)

        logger.info(f'Saved in {os.path.abspath(self.base_dir)}')

    def get_questions_codechef(self) -> List[Question]:
        logger.info(f'Downloading page https://www.codechef.com/{self.contest}')

        url = 'www.codechef.com'
        conn = HTTPSConnection(url)
        conn.request('GET', f'/api/contests/{self.contest}')
        response = conn.getresponse()
        body = response.read().decode()
        conn.close()

        if response.getcode() != 200:
            err = Exception(f'No contest found for codechef/{self.contest} ❌❌')
            raise err

        data = json.loads(body)
        questions: List[Question] = []

        caption, problems = data['name'], list(data['problems'].keys())
        logger.info(f'Found: {caption} ✅', 'Scraping problems:\n', sep='\n')

        def scrape_test_case(input_marker: str, output_marker: str, body: str):
            body_low = body.lower()
            input_idx, output_idx = body_low.find(input_marker, 0), body_low.find(output_marker, 0)
            inputs, outputs = [], []
            while input_idx != -1:
                input_start = body.find('```', input_idx)
                input_end = body.find('```', input_start + 3)
                inputs.append(body[input_start + 3: input_end])

                output_start = body.find('```', output_idx)
                output_end = body.find('```', output_start + 3)
                outputs.append(body[output_start + 3: output_end])

                input_idx = body_low.find(input_marker, input_end)
                output_idx = body_low.find(output_marker, output_end)

            return zip(inputs, outputs)

        def get_question(problem: Dict) -> Question:
            title = problem['problem_code'] + ' ' + problem['problem_name']
            time_limit = problem['max_timelimit']
            question = Question(idx, title, self.base_dir, time_limit)

            body = problem['body']
            for inp, out in scrape_test_case('example input', 'example output', body):
                question.add_test(inp, out)
            for inp, out in scrape_test_case('sample input', 'sample output', body):
                question.add_test(inp, out)

            return question

        idx, max_retries = 0, 3
        for name in problems:
            for _ in range(max_retries):
                problems_data = data.get('problems_data', None)
                problem = problems_data.get(name, None) if problems_data else None
                if problem is None or problem['status'] != 'success':
                    conn = HTTPSConnection(url)
                    conn.request('GET', f'/api/contests/{self.contest}/problems/{name}')
                    response = conn.getresponse()

                    if response.getcode() != 200:
                        conn.close()
                        break

                    problem = json.loads(response.read().decode())
                    conn.close()

                if problem['status'] == 'success':
                    question = get_question(problem)
                    questions.append(question)
                    logger.info(question)
                    idx += 1
                    break

        return questions
