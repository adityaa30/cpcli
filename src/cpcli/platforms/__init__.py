import inspect
import logging
import os
from abc import ABC, abstractmethod
from http.client import HTTPSConnection
from typing import List

from cpcli.question import Question
from cpcli.utils.config import CpCliConfig
from cpcli.utils.exceptions import InvalidProblemSetURI
from cpcli.utils.misc import walk_modules
from cpcli.utils.uri import PlatformURI

logger = logging.getLogger()


def iter_platforms(cls):
    for module in walk_modules('cpcli.platforms'):
        for obj in vars(module).values():
            if (
                    inspect.isclass(obj)
                    and issubclass(obj, cls)
                    and obj.__module__ == module.__name__
                    and not obj == cls
            ):
                yield obj


class Platform(ABC):
    def __init__(self, name: str, base_url: str, uri: PlatformURI, config: CpCliConfig) -> None:
        self.name = name
        self.base_url = base_url
        self.config = config
        self.uri = uri

    @property
    def base_dir(self) -> str:
        path = os.path.join(
            self.config.contest_files_dir,
            f'{self.name}-{self.uri.problemset}'
        )
        if not os.path.exists(path):
            logger.debug(f'Creating base directory: {path}')
            os.makedirs(path)

        return path

    @property
    def metadata_path(self) -> str:
        return os.path.join(self.base_dir, '.metadata.json')

    @classmethod
    def from_uri(cls, uri: str, config: CpCliConfig):
        platform_uri = PlatformURI(uri)
        for platform_cls in iter_platforms(cls):
            if platform_cls.uri_prefix() == platform_uri.platform:
                return platform_cls(config, platform_uri)

        raise InvalidProblemSetURI(uri)

    @staticmethod
    @abstractmethod
    def uri_prefix():
        raise NotImplementedError

    def download_response(self, request_url: str, max_retries: int = 3) -> str:
        # Establish a connection
        for _ in range(max_retries):
            conn = HTTPSConnection(self.base_url)
            conn.request('GET', request_url)
            response = conn.getresponse()
            body = response.read().decode()
            response_code = response.getcode()
            conn.close()

            if response_code != 200:
                continue

            return body

        return ''

    @abstractmethod
    def get_questions(self) -> List[Question]:
        pass
