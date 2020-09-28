import logging
from typing import List

from lxml.html import document_fromstring

from cpcli.platforms import Platform
from cpcli.question import Question
from cpcli.utils.config import CpCliConfig

logger = logging.getLogger()


class CodeForces(Platform):
    BASE_URL = 'codeforces.com'
    NAME = 'Codeforces'

    def __init__(self, config: CpCliConfig, uri: str):
        super().__init__(self.NAME, self.BASE_URL, uri, config)

    @staticmethod
    def uri_prefix():
        return 'cf'

    def get_questions(self) -> List[Question]:
        logger.info(f'Downloading page {self.base_url}/contest/{self.contest}/problems')

        response_code, body = self.download_response(f"/contest/{self.contest}/problems")
        if response_code != 200:
            err = Exception(f'No contest found for codechef/{self.contest} ❌❌')
            raise err

        questions: List[Question] = []

        doc = document_fromstring(body)
        caption = doc.xpath('//div[@class="caption"]/text()')[0]

        logger.info(f'Found: {caption} ✅')
        logger.info('Scraping problems:')

        problems = doc.xpath('//div[@class="problem-statement"]')
        for idx, problem in enumerate(problems):
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
