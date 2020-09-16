import inspect
from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import Dict

from cpcli.utils.cmdtypes import readable_dir, readable_file, contest_uri
from cpcli.utils.constants import DEFAULT_CONTEST_FILES_DIR, CONTEST_URI_HELP
from cpcli.utils.misc import walk_modules


class BaseCommand(ABC):

    def __init__(self):
        self.subcommands: Dict[str, BaseCommand] = {}
        for cmd in self.iter_subcommands():
            cmdname = cmd.__module__.split('.')[-1]
            self.subcommands[cmdname] = cmd()

    @classmethod
    def iter_subcommands(cls):
        for module in walk_modules('cpcli.commands'):
            for obj in vars(module).values():
                if (
                        inspect.isclass(obj)
                        and issubclass(obj, cls)
                        and obj.__module__ == module.__name__
                        and not obj == cls
                ):
                    yield obj

    @classmethod
    def from_parser(cls, parser: ArgumentParser):
        obj = cls()
        obj.add_options(parser)
        return obj

    def add_options(self, parser: ArgumentParser) -> None:
        """Adds new sub-commands/flags/options to the parser"""
        parser.add_argument(
            '-t', '--template',
            action='store',
            type=readable_file,
            default='Template.cpp',
            required=False,
            help='Competitive programming template file',
        )

        parser.add_argument(
            '-p', '--path',
            action='store',
            type=readable_dir,
            default=DEFAULT_CONTEST_FILES_DIR,
            required=False,
            help='Path of the dir where all input/output files are saved'
        )

        parser.add_argument(
            '-c', '--contest-uri',
            action='store',
            type=contest_uri,
            required=True,
            help=CONTEST_URI_HELP
        )

        # Update all the subparsers
        sub_parsers = parser.add_subparsers(dest='command')
        for name, subcmd in self.subcommands.items():
            subcmd_parser = sub_parsers.add_parser(name)
            subcmd.add_options(subcmd_parser)

    def process_arguments(self, args) -> None:
        """Takes in all the arguments passed to the cli.
        Preprocesses/Precomputes anything based on the arguments passed
        """
        pass

    @abstractmethod
    def run(self, args) -> None:
        """Entry point for running commands"""
        raise NotImplementedError
