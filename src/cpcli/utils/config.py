import os
from configparser import ConfigParser
from os.path import abspath, dirname, exists, expanduser, join
from typing import List, Optional

from cpcli.utils.constants import CONFIG_FILE_NAME, DEFAULT_CONTEST_FILES_DIR


def closest_cpcli_config(path: str = '.', prev_path: Optional[str] = None) -> str:
    """Return the path to the closest cpcli.ini file by traversing the current
    directory and its parents
    """
    if path == prev_path:
        return ''
    path = abspath(path)
    config_file = join(path, CONFIG_FILE_NAME)
    if exists(config_file):
        return config_file
    return closest_cpcli_config(dirname(path), path)


def get_config(use_closest: bool = True) -> ConfigParser:
    sources = get_sources(use_closest)
    cfg = ConfigParser()
    cfg.read(sources)
    return cfg


def get_sources(use_closest: bool = True) -> List[str]:
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or expanduser('~/.config')
    sources = [
        f'/etc/{CONFIG_FILE_NAME}',
        fr'c:\cpcli\{CONFIG_FILE_NAME}',
        xdg_config_home + f'/{CONFIG_FILE_NAME}',
        expanduser(f'~/.{CONFIG_FILE_NAME}'),
    ]
    if use_closest:
        sources.append(closest_cpcli_config())
    return sources


class CpCliConfig:
    def __init__(self):
        self.config = get_config()
        self._config_path = closest_cpcli_config()

    @property
    def root_dir(self):
        if not self._config_path:
            raise FileNotFoundError(
                f'{CONFIG_FILE_NAME} not found. Declare this or any parent '
                f'directory as project directory first using `cpcli init .`'
            )
        return abspath(dirname(self._config_path))

    @property
    def contest_files_dir(self) -> str:
        return join(self.root_dir, DEFAULT_CONTEST_FILES_DIR)
