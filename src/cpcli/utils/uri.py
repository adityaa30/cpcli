from typing import Optional

from cpcli.utils.exceptions import InvalidProblemSetURI


class PlatformURI:
    def __init__(self, uri: str):
        self._uri = uri
        self.uri = uri.strip().split('::')
        if not 2 <= len(self.uri) <= 3:
            raise InvalidProblemSetURI(uri)

    @property
    def platform(self):
        return self.uri[0]

    @property
    def problemset(self):
        return self.uri[1]

    @property
    def problem(self) -> Optional[str]:
        if len(self.uri) == 3:
            return self.uri[2]
        return None

    @property
    def problem_specific_uri(self) -> bool:
        return len(self.uri) == 3

    def __str__(self):
        return self._uri

    __repr__ = __str__
