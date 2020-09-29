import json
import logging
import os
import shutil
from subprocess import Popen, PIPE
from typing import Optional, List, Dict

from cpcli.platforms import Platform
from cpcli.question import Question
from cpcli.utils.config import CpCliConfig
from cpcli.utils.exceptions import InvalidProblemSetURI

logger = logging.getLogger()


class Runner:
    def __init__(self, uri: str, template: str, config: CpCliConfig) -> None:
        self.uri = uri
        self.config = config
        self.platform = Platform.from_uri(uri, config)
        self.base_dir = self.platform.base_dir

        self.template = template

        self.questions: List[Question] = []

    def to_dict(self) -> Dict:
        metadata: Dict = {
            'platform': self.platform.name,
            'problemset': self.platform.uri.problemset,
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
            logging.info(question)
            if verbose:
                for test in question.test_cases:
                    logging.info(test)

    def run_test_cases(self, val: str, file: Optional[str] = None) -> None:
        question = self.get_question(val)

        if not question:
            logger.warning('Invalid question entered. Following are available:')
            for question in self.questions:
                logger.warning(f"[{question.idx}]\t{question.title}")
            return

        if file and not os.path.exists(file):
            logger.warning(f'"{file}" solution file do not exist')
            return

        logger.info(f'Checking question: {question.title}')

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
        if force_download or (not os.path.exists(self.platform.metadata_path)):
            try:
                self.questions = self.platform.get_questions()
            except InvalidProblemSetURI as err:
                logger.error(err)

            self.save_questions()
            return

        self.questions = []
        with open(self.platform.metadata_path, 'r') as file:
            metadata = json.load(file)

        for question in metadata['questions']:
            self.questions.append(Question.from_dict(question))

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
        with open(self.platform.metadata_path, 'w') as file:
            json.dump(self.metadata, file, indent=2)

        logger.info(f'Saved in {os.path.abspath(self.base_dir)}')
