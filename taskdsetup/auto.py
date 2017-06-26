
import os
import shutil
from typing import List
from . import (core, init, user, client)
from .core import canonicalize

def dispatcher(data: str, dns_name: str, expr: dict) -> None:
    cmd = expr['cmd']
    if cmd == None:
        pass
    elif cmd == 'os.makedirs':
        os.makedirs(expr['dir'])
    elif cmd == 'configure':
        core.configure(data, [expr['var'], expr['value']])
    elif cmd == 'shutil.copy2':
        shutil.copy2(expr['from'], expr['to'])
    elif cmd == 'pki_call':
        core.pki_call(data, expr['script'])
    elif cmd == 'change_cn_line':
        core.change_cn_line(data=data, cn=dns_name)
    elif cmd == 'shutil.copytree':
        shutil.copytree(expr['source'], expr['dest'])
    elif cmd == 'taskd_call':
        core.taskd_call(data, expr['args'])
    elif cmd == 'print':
        print(expr['str'])
    elif cmd == 'task_config':
        core.task_config(expr['var'], expr['value'])

def cli_init(data, source, dns_name, internal_ip, port):

    cert_names = [ 'client.cert', 'client.key',
                   'server.cert', 'server.key', 'server.crl', 'ca.cert' ]

    cert_files = [ os.path.join(data, 'pki', n + '.pem')
                   for n in cert_names ]

    all_exist = all(map(os.path.isfile, cert_files))

    if source == None:
        source = os.path.join(core.return_project_base_dir(), 'taskd')

    source_pki = os.path.join(source, 'pki')
    data_pki = os.path.join(data, 'pki')

    data_pki_exists = os.path.exists(data_pki)

    data_exists = os.path.isdir(data)

    exprs = init.main(data=data, data_exists=data_exists,
                      source_pki=source_pki,
                      data_pki=data_pki, data_pki_exists=data_pki_exists,
                      server=internal_ip, port=port,
                      cert_names=cert_names, cert_files=cert_files,
                      all_exist=all_exist)

    for expr in exprs:
        print(expr)
        dispatcher(data=data, dns_name=dns_name, expr=expr)

def cli_user(data: str, orgs: dict):
    data_orgs_dict = core.get_dict_of_users(data=data)
    user_keys_list = core.get_user_keys_list(data=data)
    exprs = user.main(config_orgs_dict=orgs, data_orgs_dict=data_orgs_dict,
                      user_keys_list=user_keys_list)

    for expr in exprs:
        dispatcher(data=data, dns_name=None, expr=expr)
        # print(expr)

def cli_client(data: str, dns_name: str, port: str):
    task_dir = os.path.expanduser('~/.task')
    d = core.get_dict_of_users(data=data)
    result = [] # type: List[dict]
    for org in d:
        for uuid in d[org]:
            full_name = d[org][uuid]
            user_name = canonicalize(full_name)
            for cert in [ user_name + '.cert.pem',
                          user_name + '.key.pem',
                          'ca.cert.pem' ]:
                source = os.path.join(data, 'pki', cert)
                result += [ { 'cmd': 'shutil.copy',
                              'src': source,
                              'dest': task_dir } ]

            result += client.main(user_name=user_name, server=dns_name,
                                  port=port, org=org, full_name=full_name,
                                  uuid=uuid)
    for expr in result:
        dispatcher(data=data, dns_name=None, expr=expr)
        # print(expr)
