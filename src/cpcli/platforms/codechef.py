import json
import logging
from typing import Dict, Iterator, List, Tuple

from cpcli.platforms import Platform
from cpcli.question import Question
from cpcli.utils.config import CpCliConfig

logger = logging.getLogger()


class CodeChef(Platform):
    BASE_URL = 'www.codechef.com'
    NAME = 'CodeChef'

    def __init__(self, config: CpCliConfig, uri: str):
        super().__init__(self.NAME, self.BASE_URL, uri, config)

    @staticmethod
    def uri_prefix():
        return 'cc'

    @staticmethod
    def _scape_test_cases(
            input_marker: str,
            output_marker: str,
            body: str
    ) -> Iterator[Tuple[str, str]]:
        body_low = body.lower()
        input_idx = body_low.find(input_marker, 0)
        output_idx = body_low.find(output_marker, 0)
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

    def parse_question(self, idx: int, problem: Dict) -> Question:
        title = problem['problem_code'] + ' ' + problem['problem_name']
        time_limit = problem['max_timelimit']
        question = Question(idx, title, self.base_dir, time_limit)

        body = problem['body']
        for inp, out in self._scape_test_cases('example input', 'example output', body):
            question.add_test(inp, out)
        for inp, out in self._scape_test_cases('sample input', 'sample output', body):
            question.add_test(inp, out)

        return question

    def get_questions(self) -> List[Question]:
        logger.info(f'Downloading page {self.BASE_URL}/{self.contest}')

        response_code, body = self.download_response(f'/api/contests/{self.contest}')
        if response_code != 200:
            err = Exception(f'No contest found for codechef/{self.contest} ❌❌')
            raise err

        data = json.loads(body)
        questions: List[Question] = []

        caption, problems = data['name'], list(data['problems'].keys())
        logger.info(f'Found: {caption} ✅')
        logger.info('Scraping problems:')

        idx = 0
        max_retries = 3

        for name in problems:
            for _ in range(max_retries):
                problems_data = data.get('problems_data', None)
                problem = problems_data.get(name, None) if problems_data else None

                if problem is None or problem['status'] != 'success':
                    problem_response_code, problem_body = self.download_response(
                        f'/api/contests/{self.contest}/problems/{name}'
                    )
                    if problem_response_code != 200:
                        break
                    problem = json.loads(problem_body)

                if problem['status'] == 'success':
                    question = self.parse_question(idx, problem)
                    questions.append(question)
                    logger.info(question)
                    idx += 1
                    break

        return questions
