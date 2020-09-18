class InvalidContestURI(TypeError):
    def __init__(self, uri: str) -> None:
        self.uri = uri

    def __str__(self):
        return f'InvalidContestURI: {self.uri} is not a valid contest uri'
