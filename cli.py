import os
from http.client import HTTPSConnection
from typing import Tuple, List
from pprint import pformat
from argparse import ArgumentParser
from lxml.html import document_fromstring


parser = ArgumentParser(description='Competitive Programming Helper')


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
    def __init__(self, platform: str, contest: str) -> None:
        self.platform = platform
        self.contest = contest

        if platform == 'cf':
            self.questions = self.get_questions_codeforces()
        elif platform == 'cc':
            self.questions = self.get_questions_codechef()

    @staticmethod
    def kebab_case(val: str) -> str:
        words = [
            ''.join(c for c in word.strip() if c.isalnum())
            for word in val.strip().split(' ')
        ]
        return '-'.join(words)

    def get_questions_codeforces(self) -> List:
        url = f'codeforces.com'
        conn = HTTPSConnection(url)
        conn.request("GET", f"/contest/{self.contest}/problems")
        html = conn.getresponse().read().decode()
        conn.close()
        questions = []

        doc = document_fromstring(html)
        problems = doc.xpath('//div[@class="problem-statement"]')
        for problem in problems:
            title = problem.find_class("title")[0].text_content()
            sample_tests = problem.find_class("sample-test")[0]
            inputs = sample_tests.find_class('input')
            outputs = sample_tests.find_class('output')
            test_cases = []

            for inp, out in zip(inputs, outputs):
                sample_input = inp.xpath('descendant-or-self::pre/text()')[0]
                sample_output = out.xpath('descendant-or-self::pre/text()')[0]
                test_cases.append((sample_input, sample_output))

            questions.append({
                'title': title,
                'sample-tests': test_cases
            })

        return questions

    def write_to(self, root_dir: str) -> None:
        base = os.path.join(root_dir, str(self.contest))
        for question in self.questions:
            title = self.kebab_case(question['title'])
            question_dir = os.path.join(base, title)
            input_dir = os.path.join(question_dir, 'Input')
            output_dir = os.path.join(question_dir, 'Output')

            os.path.exists(input_dir) or os.makedirs(input_dir)
            os.path.exists(output_dir) or os.makedirs(output_dir)

            for idx, (sample_input, sample_output) in enumerate(question['sample-tests'], start=1):
                input_path = os.path.join(input_dir, f'{idx}.txt')
                output_path = os.path.join(output_dir, f'{idx}.txt')

                with open(input_path, 'w') as f:
                    f.write(sample_input)

                with open(output_path, 'w') as f:
                    f.write(sample_output)

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


def contest_uri(uri):
    return Platforms.parse(uri)


parser.add_argument(
    '-p', '--path',
    action='store',
    type=readable_dir,
    default=CONTEST_FILES_DIR,
    required=False,
    help='Path of the dir where all input/output files are saved'
)

parser.add_argument(
    '-c', '--contest-uri',
    action='store',
    type=contest_uri,
    required=True,
    help=CONTEST_URI_HELP
)

args = parser.parse_args()

scraper = Scraper(args.contest_uri[0], args.contest_uri[1])
scraper.write_to(args.path)
