
import argparse
from . import (init, keys, user, user_keys, config)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--data', default='/tmp/var/taskd')
    subparsers = parser.add_subparsers(dest='cmd')

    parser_init = subparsers.add_parser('init')
    parser_init.add_argument('--source')
    parser_init.add_argument('--cn', default='localhost')
    parser_init.add_argument('--server', default='localhost')

    parser_keys = subparsers.add_parser('keys')

    parser_user = subparsers.add_parser('user')
    parser_user.add_argument('--org', default='Public')
    parser_user.add_argument('--user', default='Testing')

    parser_user_keys = subparsers.add_parser('user_keys')
    parser_user_keys.add_argument('--user-name', default='testing')

    parser_config = subparsers.add_parser('config')
    parser_config.add_argument('--site', default='localhost')
    parser_config.add_argument('--port', default='53589')
    parser_config.add_argument('--dot-task', default='/tmp/.task')

    args = parser.parse_args()
    if args.cmd == 'init':
        init.main(args.data, args.source, args.cn, args.server)
    elif args.cmd == 'keys':
        keys.main(args.data)
    elif args.cmd == 'user':
        user.main(args.data, args.org, args.user)
    elif args.cmd == 'user_keys':
        user_keys.main(args.data, args.user_name)
    elif args.cmd == 'config':
        config.main(args.data, args.site, args.port, args.dot_task)
