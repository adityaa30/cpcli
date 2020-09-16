from argparse import ArgumentParser

from cpcli.commands import BaseCommand


def execute():
    parser = ArgumentParser(description='Competitive Programming Helper')
    command = BaseCommand.from_parser(parser)
    args = parser.parse_args()
    command.run(args)
