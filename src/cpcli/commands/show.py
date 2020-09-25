import logging
from argparse import ArgumentParser, Namespace

from zope.interface import implementer

from cpcli.commands import ICommand
from cpcli.runner import Runner

logger = logging.getLogger()


@implementer(ICommand)
class ShowCommand:
    def add_options(self, parser: ArgumentParser) -> None:
        parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            required=False,
            default=False,
            help='If True show all test cases (default=False)'
        )
        parser.add_argument(
            '-q', '--question',
            action='store',
            required=False,
            help='Shows only test cases of the provided question'
        )

    def run(self, args: Namespace, runner: Runner) -> None:
        if args.question:
            question = runner.get_question(args.question)

            if not question:
                logger.warning('Invalid question entered. Following are available:')
                runner.show_all_questions()
            else:
                logger.info(question)
                for tst in question.test_cases:
                    logger.info(tst)

        else:
            runner.show_all_questions(verbose=args.verbose)
