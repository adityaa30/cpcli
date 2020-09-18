import inspect
from argparse import ArgumentParser, ArgumentError, Namespace
from contextlib import suppress
from typing import Dict, Optional

from zope.interface import Interface, implementer
from zope.interface.exceptions import Invalid, MultipleInvalid
from zope.interface.verify import verifyClass

from cpcli.scrapper import Scraper
from cpcli.utils.cmdtypes import readable_file, contest_uri
from cpcli.utils.config import CpCliConfig
from cpcli.utils.constants import CONTEST_URI_HELP
from cpcli.utils.misc import walk_modules


class ICommand(Interface):
    def add_options(parser: ArgumentParser) -> None:
        pass

    def run(args: Namespace, scraper: Scraper) -> None:
        pass


def iter_subcommands(cls):
    for module in walk_modules('cpcli.commands'):
        for obj in vars(module).values():
            with suppress(Invalid, MultipleInvalid):
                if (
                        inspect.isclass(obj)
                        and verifyClass(ICommand, obj)
                        and obj.__module__ == module.__name__
                        and not obj == cls
                ):
                    yield obj


@implementer(ICommand)
class BaseCommand:

    def __init__(self):
        self.subcommands: Dict[str, BaseCommand] = {}
        for cmd in iter_subcommands(BaseCommand):
            cmdname = cmd.__module__.split('.')[-1]
            self.subcommands[cmdname] = cmd()

        self.config = CpCliConfig()

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
            '-c', '--contest-uri',
            action='store',
            type=contest_uri,
            required=False,
            help=CONTEST_URI_HELP
        )

        # Update all the subparsers
        sub_parsers = parser.add_subparsers(dest='command')
        for name, subcmd in self.subcommands.items():
            subcmd_parser = sub_parsers.add_parser(name)
            subcmd.add_options(subcmd_parser)

    def load_scraper(self, args) -> Scraper:
        if not args.contest_uri:
            raise ArgumentError(None, 'the following arguments are required: -c/--contest-uri')

        return Scraper(
            platform=args.contest_uri[0],
            contest=args.contest_uri[1],
            template=args.template,
            config=self.config
        )

    def run(self, args: Namespace, scraper: Optional[Scraper] = None) -> None:
        if args.command != 'init':
            scraper = self.load_scraper(args)
            scraper.load_questions()

        if args.command:
            self.subcommands[args.command].run(args, scraper)
