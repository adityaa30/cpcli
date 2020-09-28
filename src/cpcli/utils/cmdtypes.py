import os

from cpcli.utils.constants import DEFAULT_CONTEST_FILES_DIR


def readable_dir(path):
    error = TypeError(f'readable_dir:{path} is not a valid dir')

    if path == DEFAULT_CONTEST_FILES_DIR and not os.path.exists(path):
        os.mkdir(DEFAULT_CONTEST_FILES_DIR)

    if not os.path.isdir(path):
        raise error
    if os.access(path, os.R_OK):
        return path
    else:
        raise error


def readable_file(path):
    error = TypeError(f'readable_file:{path} is not a valid file')

    if not os.path.isfile(path):
        raise error
    if os.access(path, os.R_OK):
        return os.path.abspath(path)
    else:
        raise error


def valid_uri(uri: str) -> str:
    """ToDo: URI will never have any spaces.
    """
    return uri
