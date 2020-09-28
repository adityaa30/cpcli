import logging
from subprocess import Popen, PIPE, TimeoutExpired
from typing import Dict

from cpcli.utils.constants import WHITE_SPACES
from cpcli.utils.python import compare

logger = logging.getLogger()


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
            encoding='utf-8'
        )
        message = ''
        try:
            output, err = test_process.communicate(self.sample_input, timeout=self.question.time_limit)
            if test_process.returncode == 0:
                if compare(output, self.sample_output):
                    message = '✅'
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
            logger.info(f'{"Custom" if self.custom_testcase else "Sample"} Test Case {self.idx + 1}: {message}')

    def __str__(self) -> str:
        return (
            f'Test Case: {self.idx + 1}\n'
            f'Input\n'
            f'{self.sample_input}\n\n'
            f'Output\n'
            f'{self.sample_output}\n\n'
        )

    __repr__ = __str__
