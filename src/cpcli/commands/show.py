from argparse import ArgumentParser, Namespace

from zope.interface import implementer

from cpcli.commands import ICommand
from cpcli.runner import Runner


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

    def run(self, args: Namespace, scraper: Runner) -> None:
        if args.question:
            question = scraper.get_question(args.question)

            if not question:
                print('Invalid question entered. Following are available:')
                scraper.show_all_questions()
            else:
                print(question)
                for tst in question.test_cases:
                    print(tst)

        else:
            scraper.show_all_questions(verbose=args.verbose)
