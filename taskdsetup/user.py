
import os
import subprocess
from .core import (get_dict_of_users, pki_call)

def add_org(taskddata, org):
    target = os.path.join(taskddata, 'orgs')
    if not os.path.isdir(target):
        os.mkdir(target)
    subprocess.call(['taskd','add','org',org, '--data',taskddata])

def add_user(taskddata, org, full_name):
    users = get_dict_of_users(taskddata)
    existing_full_names = [ users[org][uuid] for org in users.keys()
                            for uuid in users[org] ]
    if full_name.lower().replace(' ','_') in map(
            lambda x: x.lower().replace(' ','_'),existing_full_names):
        print("Similar name already exists")
    else:
        subprocess.call(['taskd','add','user',org,full_name, '--data',taskddata])

def add_user_keys(taskddata, user):
    user_name = user.lower().replace(' ', '_')
    if os.path.exists(os.path.join(taskddata, 'pki', user_name + '.key.pem')):
        print('User key for ' + user_name + ' already exists')
    else:
        pki_call(taskddata, ['./generate.client', user_name])

def main(data, config_orgs_dict):
    c = config_orgs_dict
    for org in c:
        add_org(data, org)
        for full_name in c[org]:
            add_user(data, org, full_name)
            user_name = full_name.lower().replace(' ', '_')
            add_user_keys(data, user_name)
