
import argparse
from .auto import (cli_init, cli_user, cli_client)

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    parser_init = subparsers.add_parser('init')
    parser_user = subparsers.add_parser('user')
    parser_config = subparsers.add_parser('client')

    args = parser.parse_args()
    if args.cmd == 'init':
        cli_init()
    elif args.cmd == 'user':
        cli_user()
    elif args.cmd == 'client':
        cli_client()
