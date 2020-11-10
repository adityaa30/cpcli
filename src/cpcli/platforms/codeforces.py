import logging
from typing import List

from lxml.html import document_fromstring

from cpcli.platforms import Platform
from cpcli.question import Question
from cpcli.utils.config import CpCliConfig
from cpcli.utils.uri import PlatformURI
from cpcli.utils.exceptions import InvalidProblemSetURI

logger = logging.getLogger()


class CodeForces(Platform):
    BASE_URL = 'codeforces.com'
    NAME = 'Codeforces'

    def __init__(self, config: CpCliConfig, uri: PlatformURI):
        super().__init__(self.NAME, self.BASE_URL, uri, config)

    @staticmethod
    def uri_prefix():
        return 'cf'

    def extra_message(self) -> str:
        extra = 'Contest does not exist \n'
        return extra

    def get_questions(self) -> List[Question]:
        contest = self.uri.problemset
        logger.info(f'Downloading page {self.base_url}/contest/{contest}/problems')

        body = self.download_response(f"/contest/{contest}/problems")
        if body is ' ':
            raise InvalidProblemSetURI(str(self.uri), self.extra_message())

        questions: List[Question] = []

        doc = document_fromstring(body)
        caption = doc.xpath('//div[@class="caption"]/text()')[0]

        logger.info(f'Found: {caption} ✅')
        logger.info('Scraping problems:')

        problems = doc.xpath('//div[@class="problem-statement"]')
        for idx, problem in enumerate(problems, start=1):
            title = problem.find_class("title")[0].text_content()
            time_limit = problem.find_class("time-limit")[0].text_content()

            time_limit = time_limit[len('time limit per test'):].split(' ')[0]
            question = Question(idx, title, self.base_dir, time_limit)

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
