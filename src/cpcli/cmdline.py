from argparse import ArgumentParser

import cpcli
from cpcli.commands import BaseCommand
from cpcli.utils.log import initialize_logger


def execute():
    initialize_logger()

    parser = ArgumentParser(description='Competitive Programming Helper')
    command = BaseCommand.from_parser(parser)
    args = parser.parse_args()
    command.run(args)

if __name__ == '__main__':
    execute()