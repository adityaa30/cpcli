import os
import shutil
import subprocess
from http.client import HTTPSConnection
from typing import Dict, Tuple, List, Optional
from pprint import pformat
from argparse import ArgumentParser
from lxml.html import document_fromstring

WHITE_SPACES = ' \n\t'


class InvalidContestURI(TypeError):
    def __init__(self, uri: str) -> None:
        self.uri = uri

    def __str__(self):
        return f'InvalidContestURI: {self.uri} is not a valid contest uri'


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

        raise TypeError(f"Invalid platform. Choose one of {self.PREFIX.keys()!r}")

    @classmethod
    def parse(cls, uri: str) -> Tuple[str]:
        idx = uri.find("::")
        if idx == -1:
            raise InvalidContestURI(uri)

        platform, contest = uri[:idx], uri[idx+2:]
        if platform not in Platforms.PREFIX or not contest.isalnum():
            raise InvalidContestURI(uri)

        return platform, contest


class Scraper:
    def __init__(self, platform: str, contest: str, template: str, root_dir: str) -> None:
        self.platform = platform
        self.contest = contest

        self.root_dir = os.path.abspath(root_dir)
        self.base_dir = os.path.join(self.root_dir, str(self.contest))

        self.template = template
        self.template_basename = os.path.basename(template)

        template_extension = os.path.splitext(self.template_basename)[1]
        self.template_save_name = f'Solve{template_extension}'

        self.questions = None

    @staticmethod
    def kebab_case(val: str) -> str:
        words = [
            ''.join(c for c in word.strip(WHITE_SPACES) if c.isalnum())
            for word in val.strip(WHITE_SPACES).split(' ')
        ]
        return '-'.join(words)

    def get_question(self, val: str) -> Optional[Dict]:
        for idx, question in enumerate(self.questions, start=0):
            if str(idx) == val or val in question['title'].lower():
                return question
        return None

    def get_question_path(self, title: str) -> Optional[str]:
        return os.path.join(self.root_dir, str(self.contest), title, self.template_save_name)

    def run_test_cases(self, val: str, file: Optional[str] = None) -> None:
        question = self.get_question(val)

        if not question:
            print('Invalid question entered. Following are available:')
            for idx, question in enumerate(self.questions, start=1):
                print(f"[{idx}]\t{question['title']}")
            return

        if file and not os.path.exists(file):
            print(f'"{file}" solution file do not exist')
            return

        print(f'[#] Checking question: {question["title"]}')

        solution_file = file or self.get_question_path(question['title'])
        question_dir = os.path.join(self.base_dir, question['title'])
        input_dir = os.path.join(question_dir, 'Input')
        output_dir = os.path.join(question_dir, 'Output')

        for idx in range(len(question['sample-tests'])):
            sample_input_path = os.path.join(input_dir, f'{idx + 1}.txt')
            sample_output_path = os.path.join(output_dir, f'{idx + 1}.txt')
            response = subprocess.run([
                f'./autocpp.sh '
                f'{solution_file} {sample_input_path} {sample_output_path}'
            ], shell=True, capture_output=True)

            output = response.stdout.decode().strip(WHITE_SPACES)
            correct = output == question['sample-tests'][idx][1]
            result = '✅' if correct else '❌'
            print(f'[#] Sample Test Case {idx + 1}: {result}')

            if not correct:
                print('Sample Input:')
                print(question['sample-tests'][idx][0], '\n')

                print('Sample Output:')
                print(question['sample-tests'][idx][1], '\n')

                print('Your Output:')
                print(output, '\n')

                errors = response.stderr.decode().strip(WHITE_SPACES)
                if errors:
                    print('Errors:')
                    print(errors, '\n')

    def load_questions(self, force_download=False) -> List:
        if force_download or (not os.path.exists(self.base_dir)):
            if self.platform == 'cf':
                self.questions = self.get_questions_codeforces()
            elif self.platform == 'cc':
                self.questions = self.get_questions_codechef()
            return

        questions = []
        titles = os.listdir(self.base_dir)
        titles.sort()
        for title in titles:
            question_dir = os.path.join(self.base_dir, title)
            input_dir = os.path.join(question_dir, 'Input')
            output_dir = os.path.join(question_dir, 'Output')

            tests = os.listdir(input_dir)
            test_cases = []

            for test in tests:
                input_path = os.path.join(input_dir, test)
                output_path = os.path.join(output_dir, test)

                with open(input_path, 'r') as f:
                    sample_input = f.read()

                with open(output_path, 'r') as f:
                    sample_output = f.read()

                test_cases.append((sample_input, sample_output))

            questions.append({
                'title': title,
                'sample-tests': test_cases
            })

        self.questions = questions

    def get_questions_codeforces(self) -> List:
        url = f'codeforces.com'
        conn = HTTPSConnection(url)
        conn.request("GET", f"/contest/{self.contest}/problems")
        response = conn.getresponse()

        if response.code != 200:
            print(f'No contest found for codeforces/{self.contest} ❌❌')
            return None

        html = response.read().decode()
        conn.close()
        questions = []

        doc = document_fromstring(html)
        caption = doc.xpath('//div[@class="caption"]/text()')[0]

        print(f'Found: {caption} ✅')
        print('Scraping problems:')

        problems = doc.xpath('//div[@class="problem-statement"]')
        for problem in problems:
            title = problem.find_class("title")[0].text_content()
            sample_tests = problem.find_class("sample-test")[0]
            inputs = sample_tests.find_class('input')
            outputs = sample_tests.find_class('output')
            test_cases = []

            for inp, out in zip(inputs, outputs):
                sample_input = inp.xpath('descendant-or-self::pre/text()')[0].strip(WHITE_SPACES)
                sample_output = out.xpath('descendant-or-self::pre/text()')[0].strip(WHITE_SPACES)
                test_cases.append((sample_input, sample_output))

            questions.append({
                'title': title,
                'sample-tests': test_cases
            })

            print(f'[#]  {title} -- {len(test_cases)} Samples')

        return questions

    def save_questions(self) -> None:
        if self.questions is None:
            return

        for num, question in enumerate(self.questions, start=1):
            title = f"{num}-{self.kebab_case(question['title'])}"
            question_dir = os.path.join(self.base_dir, title)
            input_dir = os.path.join(question_dir, 'Input')
            output_dir = os.path.join(question_dir, 'Output')

            os.path.exists(question_dir) or os.makedirs(question_dir)
            os.path.exists(input_dir) or os.makedirs(input_dir)
            os.path.exists(output_dir) or os.makedirs(output_dir)

            # Copy the template
            shutil.copy(self.template, question_dir)
            solution_file = os.path.join(question_dir, self.template_basename)
            solve_file = os.path.join(question_dir, self.template_save_name)
            os.rename(solution_file, solve_file)

            # Save the test cases
            for idx, (sample_input, sample_output) in enumerate(question['sample-tests'], start=1):
                input_path = os.path.join(input_dir, f'{idx}.txt')
                output_path = os.path.join(output_dir, f'{idx}.txt')

                with open(input_path, 'w') as f:
                    f.write(sample_input)

                with open(output_path, 'w') as f:
                    f.write(sample_output)

        print(f'Saved in {os.path.abspath(self.base_dir)}')

    def get_questions_codechef(self) -> str:
        return 'ToDo'


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
    help='Path to the C++ program file or Question Name or 1 based index'
)
run_parser.add_argument(
    '-s', '--solution-file',
    action='store',
    type=readable_file,
    required=False,
    help='Path of the program file (different from default file)'
)

args = parser.parse_args()

scraper = Scraper(args.contest[0], args.contest[1], args.template, args.path)

if args.command == 'download':
    scraper.load_questions(force_download=True)
    scraper.save_questions()
elif args.command == 'run':
    scraper.load_questions()
    scraper.run_test_cases(args.question, args.solution_file)
