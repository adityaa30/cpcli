from argparse import ArgumentParser, Namespace

from zope.interface import implementer

from cpcli.commands import ICommand
from cpcli.runner import Runner


@implementer(ICommand)
class DownloadCommand:
    def add_options(self, parser: ArgumentParser) -> None:
        pass

    def run(self, _: Namespace, runner: Runner) -> None:
        runner.load_questions(force_download=True)
