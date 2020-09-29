from typing import Optional


class InvalidProblemSetURI(TypeError):
    def __init__(self, uri: str, extra: Optional[str] = None) -> None:
        self.uri = uri
        self.extra = extra

    def __str__(self):
        message = f'InvalidProblemSetURI: {self.uri} is not a valid problem set uri'

        if self.extra:
            message += self.extra

        return message
