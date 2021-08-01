import logging
import re
from typing import List

from lxml.html import document_fromstring

from cpcli.platforms import Platform
from cpcli.question import Question
from cpcli.utils.config import CpCliConfig
from cpcli.utils.uri import PlatformURI

logger = logging.getLogger()


class AtCoder(Platform):
    BASE_URL = 'atcoder.jp'
    NAME = 'AtCoder'

    def __init__(self, config: CpCliConfig, uri: PlatformURI):
        super().__init__(self.NAME, self.BASE_URL, uri, config)

    @staticmethod
    def uri_prefix():
        return 'ac'

    def get_questions(self) -> List[Question]:
        contest = self.uri.problemset
        logger.info(f'Downloading page {self.base_url}/contests/{contest}/tasks_print')

        body = self.download_response(f"/contests/{contest}/tasks_print")
        questions: List[Question] = []

        doc = document_fromstring(body)
        caption = doc.xpath('/html/head/title')[0].text_content()

        logger.info(f'Found: {caption} ✅')
        logger.info('Scraping problems:')

        problems = doc.xpath('//div[@class="col-sm-12"]')
        for idx, problem in enumerate(problems, start=1):
            title = problem.find_class("h2")[0].text_content()
            time_limit_memory = problem.xpath('descendant-or-self::p')[0].text_content()
            try:
                time_limit = re.findall(r'Time Limit: (\d+) sec.*', time_limit_memory)[0]
            except IndexError:
                time_limit = 5

            question = Question(idx, title, self.base_dir, time_limit)

            # [4:] -> Skip the `Problem Statement`, `Constraints`, `Input`, `Output` (format)
            sample_tests = problem.find_class("lang-en")[0].find_class("part")[4:]
            inputs = sample_tests[::2]
            outputs = sample_tests[1::2]
            assert len(inputs) == len(outputs)

            for inp, out in zip(inputs, outputs):
                sample_input = inp.xpath('descendant-or-self::pre/text()')[0].strip()
                sample_output = out.xpath('descendant-or-self::pre/text()')[0].strip()
                question.add_test(sample_input, sample_output, custom_testcase=False)

            questions.append(question)
            logger.info(question)

        return questions
