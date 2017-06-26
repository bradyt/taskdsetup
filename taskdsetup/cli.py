
import argparse
from .auto import (cli_init, cli_user, cli_client)
from .get_config import get_config

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='cmd')

    parser_init = subparsers.add_parser('init')
    parser_user = subparsers.add_parser('user')
    parser_config = subparsers.add_parser('client')

    config = get_config()

    data        = config['data']
    source      = config['source']
    dns_name    = config['dns_name']
    internal_ip = config['internal_ip']
    port        = config['port']
    orgs        = config['orgs']

    args = parser.parse_args()
    if args.cmd == 'init':
        cli_init(data=data, source=source, dns_name=dns_name,
                 internal_ip=internal_ip, port=port)
    elif args.cmd == 'user':
        cli_user(data=data, orgs=orgs)
    elif args.cmd == 'client':
        cli_client(data=data, dns_name=dns_name, port=port)
