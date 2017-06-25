
import os
from .core import (get_dict_of_users, pki_call, taskd_call, canonicalize)

def add_user(data, org, full_name, data_orgs_dict):
    d = data_orgs_dict
    if canonicalize(full_name) in [ canonicalize(d[org][uuid])
                                    for org in d for uuid in d[org] ]:
        print("Similar name already exists")
    else:
        taskd_call(data, ['add', 'user', org, full_name])

def add_user_keys(data, user_name):
    if os.path.exists(os.path.join(data, 'pki', user_name + '.key.pem')):
        print('User key for ' + user_name + ' already exists')
    else:
        pki_call(data, ['./generate.client', user_name])

def main(data, config_orgs_dict, data_orgs_dict):
    c = config_orgs_dict
    for org in c:
        taskd_call(data, ['add', 'org', org])
        for full_name in c[org]:
            add_user(data, org, full_name, data_orgs_dict)
            add_user_keys(data, canonicalize(full_name))
