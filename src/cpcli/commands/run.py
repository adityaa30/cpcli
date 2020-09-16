from argparse import ArgumentParser, Namespace

from zope.interface import implementer

from cpcli.commands import ICommand
from cpcli.helpers.scrapper import Scraper
from cpcli.utils.cmdtypes import readable_file


@implementer(ICommand)
class RunCommand:
    def add_options(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            'question',
            action='store',
            type=str,
            help='Substring representing Question Name or 1 based index'
        )
        parser.add_argument(
            '-s', '--solution-file',
            action='store',
            type=readable_file,
            required=False,
            help='Path of the program file (different from default file)'
        )

    def run(self, args: Namespace, scraper: Scraper) -> None:
        scraper.run_test_cases(args.question, args.solution_file)
