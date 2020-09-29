import os
from typing import Dict, List, Optional

import math

from cpcli.testcase import TestCase
from cpcli.utils.constants import WHITE_SPACES
from cpcli.utils.misc import kebab_case


class Question:
    def __init__(self, idx: int, title: str, base_dir: str, time_limit: str = '5') -> None:
        assert idx >= 1
        self.idx = idx
        self.title = kebab_case(title)
        self.base_dir = base_dir

        try:
            self.time_limit = math.ceil(float(time_limit))
        except ValueError:
            self.time_limit = 5

        self.test_cases: List[TestCase] = []

    @property
    def path(self) -> str:
        return os.path.abspath(os.path.join(self.base_dir, f'{self.title}.cpp'))

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
        samples = 'Sample' if len(self.test_cases) == 1 else 'Samples'
        return f'Question {self.idx}: {self.title} [⏰ {self.time_limit} sec] [{len(self.test_cases)} {samples}]'

    __repr__ = __str__
