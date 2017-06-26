
import os
from typing import (List, Set)
from .core import (pki_call_d, taskd_call_d, canonicalize)

def add_user(org: str, full_name: str, data_orgs_dict: dict) -> dict:
    d = data_orgs_dict
    if canonicalize(full_name) in [ canonicalize(d[org][uuid])
                                    for org in d for uuid in d[org] ]:
        return { 'cmd': 'print',
                 'str': 'Similar name already exists' }
    else:
        return taskd_call_d(['add', 'user', org, full_name])

def add_user_keys(user_name: str, user_keys_list: Set[str]) -> dict:
    if user_name in user_keys_list:
        return { 'cmd': 'print',
                 'str': 'User key for ' + user_name + ' already exists' }
    else:
        return pki_call_d(['./generate.client', user_name])

def main(config_orgs_dict: dict, data_orgs_dict: dict,
         user_keys_list: Set[str]) -> List[dict]:
    c = config_orgs_dict
    result = [] # type: List[dict]
    for org in c:
        result.append(taskd_call_d(['add', 'org', org]))
        for full_name in c[org]:
            result += [
                add_user(org, full_name, data_orgs_dict),
                add_user_keys(canonicalize(full_name), user_keys_list)
            ]
    return result
