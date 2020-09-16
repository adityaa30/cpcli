from argparse import ArgumentParser, Namespace

from zope.interface import implementer

from cpcli.cli import Scraper
from cpcli.commands import ICommand


@implementer(ICommand)
class DownloadCommand:
    def add_options(self, parser: ArgumentParser) -> None:
        pass

    def run(self, _: Namespace, scraper: Scraper) -> None:
        scraper.load_questions(force_download=True)
