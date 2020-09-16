from argparse import ArgumentParser, Namespace

from zope.interface import implementer

from cpcli.commands import ICommand
from cpcli.helpers.scrapper import Scraper


@implementer(ICommand)
class DownloadCommand:
    def add_options(self, parser: ArgumentParser) -> None:
        pass

    def run(self, _: Namespace, scraper: Scraper) -> None:
        scraper.load_questions(force_download=True)
