import json
import math
import os
import shutil
import string
from argparse import ArgumentParser
from http.client import HTTPSConnection
from pprint import pformat
from subprocess import Popen, PIPE, TimeoutExpired
from typing import Dict, Tuple, List, Optional

from lxml.html import document_fromstring

WHITE_SPACES = string.whitespace


def multiline_input() -> str:
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break
    return '\n'.join(lines)


def compare(s1: str, s2: str) -> bool:
    remove = string.whitespace
    translation = str.maketrans(dict.fromkeys(remove))
    return s1.translate(translation) == s2.translate(translation)


class InvalidContestURI(TypeError):
    def __init__(self, uri: str) -> None:
        self.uri = uri

    def __str__(self):
        return f'InvalidContestURI: {self.uri} is not a valid contest uri'


class TestCase:
    def __init__(
            self, idx: int,
            sample_input: str, sample_output: str,
            question,
            custom_testcase: bool = False
    ) -> None:
        self.idx = idx
        self.sample_input = sample_input.strip(WHITE_SPACES)
        self.sample_output = sample_output.strip(WHITE_SPACES)
        self.question = question
        self.custom_testcase = custom_testcase

    @classmethod
    def from_dict(cls, metadata: Dict, question):
        return cls(
            idx=metadata['idx'],
            sample_input=metadata['sample_input'],
            sample_output=metadata['sample_output'],
            question=question,
            custom_testcase=metadata['custom_testcase']
        )

    def to_dict(self) -> Dict:
        return {
            'idx': self.idx,
            'sample_input': self.sample_input,
            'sample_output': self.sample_output,
            'custom_testcase': self.custom_testcase
        }

    def check_output(self, program_output) -> bool:
        return program_output == self.sample_output

    def execute(self, executable_path: str) -> None:
        test_process = Popen(
            [executable_path],
            stdout=PIPE, stdin=PIPE, stderr=PIPE,
            text=True, encoding='utf-8'
        )
        try:
            output, err = test_process.communicate(self.sample_input, timeout=self.question.time_limit)
            if test_process.returncode == 0:
                if compare(output, self.sample_output):
                    message = f'✅'
                else:
                    message = (
                        f'❌ (WA)\n'
                        f'Sample Input:\n{self.sample_input}\n\n'
                        f'Sample Output:\n{self.sample_output}\n\n'
                        f'Your Output:\n{output}\n\n'
                    )
            else:
                message = f'❌\n{err}'
        except TimeoutExpired:
            message = f'❌ (TLE) [>{self.question.time_limit} sec]'
        finally:
            print(f'[#] {"Custom" if self.custom_testcase else "Sample"} Test Case {self.idx + 1}: {message}')

    def __str__(self) -> str:
        return (
            f'Test Case: {self.idx + 1}\n'
            f'Input\n'
            f'{self.sample_input}\n\n'
            f'Output\n'
            f'{self.sample_output}\n\n'
        )

    __repr__ = __str__


class Question:
    def __init__(self, idx: int, title: str, base_dir: str, time_limit: int = 5) -> None:
        self.idx = idx
        self.title = self.kebab_case(title)
        self.base_dir = base_dir

        try:
            self.time_limit = math.ceil(float(time_limit))
        except:
            self.time_limit = 5

        self.test_cases: List[TestCase] = []

    @property
    def path(self) -> str:
        return os.path.abspath(os.path.join(self.base_dir, f'{self.title}.cpp'))

    @staticmethod
    def kebab_case(val: str) -> str:
        words = [
            ''.join(c for c in word.strip(WHITE_SPACES) if c.isalnum() or c == '-')
            for word in val.strip(WHITE_SPACES).split(' ')
        ]
        return '-'.join(words)

    @classmethod
    def from_dict(cls, metadata: Dict):
        obj = cls(
            idx=metadata['idx'],
            title=metadata['title'],
            base_dir=metadata['base_dir'],
            time_limit=metadata.get('time_limit', 5)
        )
        for test in metadata['test_cases']:
            obj.test_cases.append(TestCase.from_dict(test, obj))
        return obj

    def to_dict(self) -> Dict:
        return {
            'idx': self.idx,
            'title': self.title,
            'base_dir': self.base_dir,
            'time_limit': self.time_limit,
            'test_cases': [test.to_dict() for test in self.test_cases]
        }

    def add_test(self, sample_input: str, sample_output: str, custom_testcase: bool = False) -> None:
        test_case = TestCase(
            idx=len(self.test_cases),
            sample_input=sample_input.strip(WHITE_SPACES),
            sample_output=sample_output.strip(WHITE_SPACES),
            question=self,
            custom_testcase=custom_testcase
        )
        self.test_cases.append(test_case)

    def remove_test(self, idx: int) -> Optional[TestCase]:
        idx = int(idx)
        to_remove = None
        for testcase in self.test_cases:
            if to_remove is not None:
                testcase.idx -= 1
            elif testcase.idx == idx:
                to_remove = testcase

        if to_remove:
            self.test_cases.remove(to_remove)
        return to_remove

    def __str__(self) -> str:
        return f'Question {self.idx + 1}: {self.title} [⏰ {self.time_limit} sec] [{len(self.test_cases)} Samples]'

    __repr__ = __str__


class Platforms:
    PREFIX = {
        'cf': 'Codeforces',
        'cc': 'Codechef',
    }

    @classmethod
    def get_link(cls, platform: str, contest: str) -> str:
        if platform == 'cc':
            return f'https://www.codechef.com/{contest}'
        elif platform == 'cf':
            return f'https://codeforces.com/contest/{contest}'

        raise TypeError(f"Invalid platform. Choose one of {cls.PREFIX.keys()!r}")

    @classmethod
    def get_dir_path(cls, root_dir: str, platform: str, contest: str) -> str:
        if platform not in cls.PREFIX:
            raise TypeError(f"Invalid platform. Choose one of {cls.PREFIX.keys()!r}")

        return os.path.join(root_dir, f'{cls.PREFIX[platform]}-{contest}')

    @classmethod
    def parse(cls, uri: str) -> Tuple[str, str]:
        idx = uri.find("::")
        if idx == -1:
            raise InvalidContestURI(uri)

        platform, contest = uri[:idx], uri[idx + 2:]
        if platform not in Platforms.PREFIX or not contest.isalnum():
            raise InvalidContestURI(uri)

        return platform, contest


class Scraper:
    def __init__(self, platform: str, contest: str, template: str, root_dir: str) -> None:
        self.platform = platform
        self.contest = contest

        self.root_dir = os.path.abspath(root_dir)
        self.base_dir = Platforms.get_dir_path(self.root_dir, platform, contest)
        self.metadata_path = os.path.join(self.base_dir, '.metadata.json')

        self.template = template

        self.questions: List[Question] = []

        if not os.path.exists(self.base_dir):
            print(f'[#] Creating base directory: {self.base_dir}')
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
            print(question)
            if verbose:
                for test in question.test_cases:
                    print(test)

    def run_test_cases(self, val: str, file: Optional[str] = None) -> None:
        question = self.get_question(val)

        if not question:
            print('Invalid question entered. Following are available:')
            for question in self.questions:
                print(f"[{question.idx}]\t{question.title}")
            return

        if file and not os.path.exists(file):
            print(f'"{file}" solution file do not exist')
            return

        assert (isinstance(question, Question))
        print(f'[#] Checking question: {question.title}')

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
        with open(self.metadata_path, 'r') as f:
            metadata = json.load(f)

        for question in metadata['questions']:
            self.questions.append(Question.from_dict(question))

    def get_questions_codeforces(self) -> List[Question]:
        print(f'Downloading page https://codeforces.com/contest/{self.contest}/problems')

        url = f'codeforces.com'
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

        print(f'Found: {caption} ✅')
        print('Scraping problems:')

        problems = doc.xpath('//div[@class="problem-statement"]')
        for idx, problem in enumerate(problems):
            title = problem.find_class("title")[0].text_content()
            time_limit = problem.find_class("time-limit")[0].text_content()
            time_limit = int(time_limit[len('time limit per test'):].split(' ')[0])

            question = Question(idx, title, self.base_dir, time_limit)

            sample_tests = problem.find_class("sample-test")[0]
            inputs = sample_tests.find_class('input')
            outputs = sample_tests.find_class('output')

            for inp, out in zip(inputs, outputs):
                sample_input = inp.xpath('descendant-or-self::pre/text()')[0]
                sample_output = out.xpath('descendant-or-self::pre/text()')[0]
                question.add_test(sample_input, sample_output)

            questions.append(question)
            print(question)

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
        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=2)

        print(f'Saved in {os.path.abspath(self.base_dir)}')

    def get_questions_codechef(self) -> List[Question]:
        print(f'Downloading page https://www.codechef.com/{self.contest}')

        url = f'www.codechef.com'
        conn = HTTPSConnection(url)
        conn.request('GET', f'/api/contests/{self.contest}')
        response = conn.getresponse()

        if response.getcode() != 200:
            err = Exception(f'No contest found for codechef/{self.contest} ❌❌')
            conn.close()
            raise err

        data = json.loads(response.read().decode())
        conn.close()
        questions: List[Question] = []

        caption = data['name']
        print(f'Found: {caption} ✅')
        print('Scraping problems:')
        problems = list(data['problems'].keys())

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

                input_idx, output_idx = body_low.find(input_marker, input_end), body_low.find(output_marker, output_end)

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
                    print(question)
                    idx += 1
                    break

        return questions


CONTEST_URI_HELP = f'''
Uri format should be: <platform-prefix>::<contest-name>
Contest Prefixes Supported: {pformat(Platforms.PREFIX)}
Eg:
\tCodeforces: cf::1382
\tCodechef: cc::JUNE20A
'''

CONTEST_FILES_DIR = 'ContestFiles'


def readable_dir(path):
    error = TypeError(f'readable_dir:{path} is not a valid dir')

    if path == CONTEST_FILES_DIR and not os.path.exists(path):
        os.mkdir(CONTEST_FILES_DIR)

    if not os.path.isdir(path):
        raise error
    if os.access(path, os.R_OK):
        return path
    else:
        raise error


def readable_file(path):
    error = TypeError(f'readable_file:{path} is not a valid file')

    if not os.path.isfile(path):
        raise error
    if os.access(path, os.R_OK):
        return os.path.abspath(path)
    else:
        raise error


def contest_uri(uri):
    return Platforms.parse(uri)


if __name__ == '__main__':
    parser = ArgumentParser(description='Competitive Programming Helper')
    parser.add_argument(
        '-t', '--template',
        action='store',
        type=readable_file,
        default='Template.cpp',
        required=False,
        help='Competitive programming template file',
    )

    parser.add_argument(
        '-p', '--path',
        action='store',
        type=readable_dir,
        default=CONTEST_FILES_DIR,
        required=False,
        help='Path of the dir where all input/output files are saved'
    )

    parser.add_argument(
        '-c', '--contest',
        action='store',
        type=contest_uri,
        required=True,
        help=CONTEST_URI_HELP
    )

    sub_parsers = parser.add_subparsers(dest='command')
    download_parser = sub_parsers.add_parser('download')
    run_parser = sub_parsers.add_parser('run')
    run_parser.add_argument(
        'question',
        action='store',
        type=str,
        help='Substring representing Question Name or 1 based index'
    )
    run_parser.add_argument(
        '-s', '--solution-file',
        action='store',
        type=readable_file,
        required=False,
        help='Path of the program file (different from default file)'
    )

    show_parser = sub_parsers.add_parser('show')
    show_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        required=False,
        default=False,
        help='If True show all test cases (default=False)'
    )
    show_parser.add_argument(
        '-q', '--question',
        action='store',
        required=False,
        help='Shows only test cases of the provided question'
    )

    testcase = sub_parsers.add_parser('testcase')
    testcase.add_argument(
        '-q', '--question',
        action='store',
        required=True,
        help='Substring representing Question Name or 1 based index'
    )
    testcase_group = testcase.add_mutually_exclusive_group()
    testcase_group.add_argument(
        '-a', '--add',
        action='store_true',
        required=False,
        default=False,
        help='Add a new custom test case'
    )
    testcase_group.add_argument(
        '-d', '--delete',
        action='store',
        required=False,
        help='Add a new custom test case'
    )

    args = parser.parse_args()

    scraper = Scraper(args.contest[0], args.contest[1], args.template, args.path)
    scraper.load_questions(force_download=(args.command == 'download'))

    if args.command == 'run':
        scraper.run_test_cases(args.question, args.solution_file)
    elif args.command == 'show':
        if args.question:
            question = scraper.get_question(args.question)

            if not question:
                print('Invalid question entered. Following are available:')
                scraper.show_all_questions()
            else:
                print(question)
                for tst in question.test_cases:
                    print(tst)

        else:
            scraper.show_all_questions(verbose=args.verbose)

    elif args.command == 'testcase':
        question = scraper.get_question(args.question)

        if not question:
            print('Invalid question entered. Following are available:')
            scraper.show_all_questions()
        else:
            print(f'Selected: {question.title}')
            if args.add:
                print(f'Enter Sample Input:  (leave empty line to submit)')
                sample_input = multiline_input()
                print(f'Enter Sample Output:  (leave empty line to submit)')
                sample_output = multiline_input()

                question.add_test(sample_input, sample_output, custom_testcase=True)
                scraper.save_questions()
            elif args.delete:
                test = question.remove_test(args.delete)
                if test is not None:
                    print(f'Deleted {test}')
                    scraper.save_questions()
                else:
                    print(f'[#] No valid test with idx={args.delete} found ❗')
            else:
                print('[#] No option chosen ❗')
