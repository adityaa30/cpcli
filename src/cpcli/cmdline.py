import sys
from argparse import ArgumentParser

from cpcli.commands import BaseCommand


def execute(argv=None):
    if argv is None:
        argv = sys.argv
    parser = ArgumentParser(description='Competitive Programming Helper')
    command = BaseCommand.from_parser(parser)
    print(argv, command.subcommands)
