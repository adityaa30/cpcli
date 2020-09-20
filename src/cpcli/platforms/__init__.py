import os

from typing import Tuple
from cpcli.utils.exceptions import InvalidContestURI


class Platforms:
    PREFIX = {
        'cf': 'Codeforces',
        'cc': 'Codechef',
    }

    @classmethod
    def get_link(cls, platform: str, contest: str) -> str:
        if platform == 'cc':
            return f'https://www.codechef.com/{contest}'
        elif platform == 'cf':
            return f'https://codeforces.com/contest/{contest}'

        raise TypeError(f"Invalid platform. Choose one of {cls.PREFIX.keys()!r}")

    @classmethod
    def get_dir_path(cls, root_dir: str, platform: str, contest: str) -> str:
        if platform not in cls.PREFIX:
            raise TypeError(f"Invalid platform. Choose one of {cls.PREFIX.keys()!r}")

        return os.path.join(root_dir, f'{cls.PREFIX[platform]}-{contest}')

    @classmethod
    def parse(cls, uri: str) -> Tuple[str, str]:
        idx = uri.find("::")
        if idx == -1:
            raise InvalidContestURI(uri)

        platform, contest = uri[:idx], uri[idx + 2:]
        if platform not in Platforms.PREFIX or not contest.isalnum():
            raise InvalidContestURI(uri)

        return platform, contest
