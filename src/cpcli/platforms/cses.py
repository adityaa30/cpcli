import logging
from typing import List, Optional

from lxml.html import document_fromstring

from cpcli.platforms import Platform
from cpcli.question import Question
from cpcli.utils.config import CpCliConfig
from cpcli.utils.exceptions import InvalidProblemSetURI
from cpcli.utils.misc import initials

logger = logging.getLogger()


class CSESProblem:
    def __init__(self, idx: int, name: str, url: str):
        assert idx >= 1
        self.idx = idx
        self.name = name
        self.url = url

    def __str__(self):
        return f"Problem {self.idx}: {self.name}"

    __repr__ = __str__


class CSESCategory:
    def __init__(self, idx: int, name: str, problems: List[CSESProblem]):
        assert idx >= 1
        self.idx = str(idx)
        self.name = name.strip()
        self.problems = problems

    def __str__(self):
        return f"Set {self.idx}: {self.name} [{len(self.problems)} Problems]"


class CSESProblemSet(Platform):
    BASE_URL = 'cses.fi'
    NAME = 'CSESProblemSet'

    def __init__(self, config: CpCliConfig, uri: str):
        super().__init__(self.NAME, self.BASE_URL, uri, config)
        self.categories: List[CSESCategory] = []

        page_html = self.download_response(f"/problemset/")
        doc = document_fromstring(page_html)

        # [1:] -> Skip the `General` heading
        headings = doc.xpath('//h2/text()')[1:]
        tasks = doc.xpath('//ul[@class="task-list"]')[1:]

        for idx, (heading, task) in enumerate(zip(headings, tasks), start=1):
            xpath_problems = task.xpath('descendant-or-self::a')
            problems: List[CSESProblem] = []
            for p_idx, problem in enumerate(xpath_problems, start=1):
                problems.append(CSESProblem(
                    p_idx,
                    problem.xpath('text()')[0],
                    problem.xpath('@href')[0],
                ))

            self.categories.append(CSESCategory(
                idx=idx,
                name=heading,
                problems=problems
            ))

    def get_category(self) -> Optional[CSESCategory]:
        # Check for initials first
        for category in self.categories:
            initial = initials(category.name.lower())
            if initial == self.uri.problemset:
                return category

        # Check if any category/problemset matches
        for idx, category in enumerate(self.categories, start=1):
            if (
                    str(idx) == category.idx
                    or category.name.lower().find(self.uri.problemset) != -1
            ):
                return category

        return None

    def get_problem(self, category: CSESCategory) -> Optional[CSESProblem]:
        if not self.uri.problem_specific_uri:
            return None

        for problem in category.problems:
            initial = initials(problem.name)
            if initial == self.uri.problem:
                return problem

        for idx, problem in enumerate(category.problems, start=1):
            if (
                    str(idx) == self.uri.problem
                    or problem.name.lower().find(self.uri.problem) != -1
            ):
                return problem

        return None

    def extra_description_categories(self) -> str:
        extra = 'No Problem Set category matched. Following are available:\n'

        for category in self.categories:
            extra += f'{category}\n'

        extra += (
            f'\nYou can put:\n'
            f'1. Set Number\n'
            f'2. Substring of the respective problem set.\n'
            f'3. Initials of the respective problem set.\n'
            f'Eg: "Introductory Problems" could be matched using '
            f'"cses::1" or "cses::intro" or "cses::ip" \n'
        )

        extra += (
            f'\nOptionally you can specify a problem too with the same format as above\n'
            f'Eg: "Weird Algorithms" problem in "Introductory Problems" could be matched  using '
            f'"cses::1::1" or "cses::1::weird" or "cses::1::wa"\n'
            f'Problems having same initials could lead to unexpected results.\n'
        )

        return extra

    def extra_description_problem(self, category: CSESCategory) -> str:
        extra = f'No Problem from "{category.name}" category matched. Following are available:\n'

        for problem in category.problems:
            extra += f'{problem}\n'

        extra += (
            f'\nYou can put:\n'
            f'1. Problem Number\n'
            f'2. Substring of the respective problem name.\n'
            f'3. Initials of the respective problem set.\n'
            f'Eg: "Weird Algorithms" problem in "Introductory Problems" could be matched  using '
            f'"cses::1::1" or "cses::1::weird" or "cses::1::wa" \n'
        )

        return extra

    @staticmethod
    def uri_prefix():
        return 'cses'

    def download_question(self, idx: int, problem: CSESProblem) -> Question:
        problem_html = self.download_response(problem.url)
        doc = document_fromstring(problem_html)
        time_limit = doc.xpath('//ul[@class="task-constraints"]/li[1]/text()')[0]
        # time = ' 1.00 s' -> 1.00
        time_limit = time_limit.strip()[:-1].strip()
        question = Question(idx, problem.name, self.base_dir, time_limit)

        # Fetch the samples
        curr_idx = 0
        while curr_idx != -1:
            start_idx = problem_html.find('Input:', curr_idx)
            end_idx = problem_html.find('</code>', start_idx) + 7
            input_html = problem_html[start_idx:end_idx]

            start_idx = problem_html.find('Output:', end_idx + 1)
            end_idx = problem_html.find('</code>', start_idx) + 7
            output_html = problem_html[start_idx:end_idx]

            sample_input = document_fromstring(input_html).xpath('//code/text()')
            sample_output = document_fromstring(output_html).xpath('//code/text()')

            if type(sample_input) == list:
                sample_input = '\n'.join(sample_input)

            if type(sample_output) == list:
                sample_output = '\n'.join(sample_output)

            question.add_test(sample_input, sample_output)
            curr_idx = problem_html.find('Input:', end_idx + 1)

        logger.info(question)

        return question

    def get_questions(self) -> List[Question]:
        category = self.get_category()
        if category is None:
            raise InvalidProblemSetURI(str(self.uri), self.extra_description_categories())

        questions: List[Question] = []

        if self.uri.problem_specific_uri:
            problem = self.get_problem(category)
            if problem is None:
                raise InvalidProblemSetURI(str(self.uri), self.extra_description_problem(category))
            else:
                logger.info(f'Downloading problem "{problem.name}" from {category.name}')
                question = self.download_question(1, problem)
                questions.append(question)
        else:
            logger.info(f'Downloading {len(category.problems)} problems from "{category.name}"')
            for idx, problem in enumerate(category.problems, start=1):
                question = self.download_question(idx, problem)
                questions.append(question)

        return questions
