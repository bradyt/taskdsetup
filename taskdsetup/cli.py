
import argparse
from . import auto
# from . import (auto init, user, client)

def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument('-d', '--data', default='/tmp/var/taskd')
    subparsers = parser.add_subparsers(dest='cmd')

    parser_init = subparsers.add_parser('init')

    parser_user = subparsers.add_parser('user')

    parser_config = subparsers.add_parser('client')

    args = parser.parse_args()
    if args.cmd == 'init':
        auto.cli_init()
    elif args.cmd == 'user':
        auto.cli_user()
    elif args.cmd == 'client':
        auto.cli_client()
