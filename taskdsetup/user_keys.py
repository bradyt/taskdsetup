
import os
from .core import pki_call

def add_user_keys(taskddata, user):
    user_name = user.lower().replace(' ', '_')
    if os.path.exists(os.path.join(taskddata, 'pki', user_name + '.key.pem')):
        print('User key for ' + user_name + ' already exists')
    else:
        pki_call(taskddata, ['./generate.client', user_name])

def main(data, config_orgs_dict):
    c = config_orgs_dict
    for org in c:
        for full_name in c[org]:
            user_name = full_name.lower().replace(' ', '_')
            add_user_keys(data, user_name)
