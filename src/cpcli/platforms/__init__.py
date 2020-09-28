import inspect
import logging
import os
from abc import ABC, abstractmethod
from http.client import HTTPSConnection
from typing import List, Tuple

from cpcli.question import Question
from cpcli.utils.config import CpCliConfig
from cpcli.utils.exceptions import InvalidContestURI
from cpcli.utils.misc import walk_modules

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
    def __init__(self, name: str, base_url: str, uri: str, config: CpCliConfig) -> None:
        self.name = name
        self.base_url = base_url
        self.config = config
        self.uri = uri
        self.base_dir = os.path.join(config.contest_files_dir, f'{self.name}-{self.contest}')
        self.metadata_path = os.path.join(self.base_dir, '.metadata.json')

        if not os.path.exists(self.base_dir):
            logger.debug(f'Creating base directory: {self.base_dir}')
            os.makedirs(self.base_dir)

    @classmethod
    def from_uri(cls, uri: str, config: CpCliConfig):
        idx = uri.find("::")
        if idx == -1:
            raise InvalidContestURI(uri)
        platform = uri[:idx]

        for platform_cls in iter_platforms(cls):
            if platform_cls.uri_prefix() == platform:
                return platform_cls(config, uri)

        raise InvalidContestURI(uri)

    @staticmethod
    @abstractmethod
    def uri_prefix():
        pass

    @property
    def contest(self):
        idx = self.uri.find('::')
        return self.uri[idx + 2:]

    def download_response(self, request_url: str) -> Tuple[int, str]:
        # Establish a connection
        conn = HTTPSConnection(self.base_url)
        conn.request('GET', request_url)
        response = conn.getresponse()
        body = response.read().decode()
        response_code = response.getcode()
        conn.close()

        return response_code, body

    @abstractmethod
    def get_questions(self) -> List[Question]:
        pass
