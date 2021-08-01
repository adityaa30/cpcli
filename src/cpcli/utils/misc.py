from importlib import import_module
from pkgutil import iter_modules

from cpcli.utils.constants import WHITE_SPACES


def walk_modules(path):
    """Loads a module and all its submodules from the given module path and
    returns them. If *any* module throws an exception while importing, that
    exception is thrown back.
    For example: walk_modules('cpcli.commands')
    """

    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, sub_path, is_package in iter_modules(mod.__path__):
            full_path = path + '.' + sub_path
            if is_package:
                mods += walk_modules(full_path)
            else:
                sub_module = import_module(full_path)
                mods.append(sub_module)
    return mods


def kebab_case(val: str) -> str:
    words = [
        ''.join(c for c in word.strip(WHITE_SPACES) if c.isalnum())
        for word in val.strip(WHITE_SPACES).split(' ')
    ]
    words = [word for word in words if word]
    return '-'.join(words)


def initials(val: str) -> str:
    return ''.join([
        word[0]
        for word in val.split(' ')
    ])
