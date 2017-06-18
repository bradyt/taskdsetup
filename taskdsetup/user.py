
import os
import subprocess
from .core import (get_dict_of_users, pki_call)

def add_org(taskddata, org):
    target = os.path.join(taskddata, 'orgs')
    if not os.path.isdir(target):
        os.mkdir(target)
    subprocess.call(['taskd','add','org',org,
                     '--data',taskddata])

def add_user(taskddata, org, full_name):
    users = get_dict_of_users(taskddata)
    existing_full_names = [ users[org][uuid] for org in users.keys()
                            for uuid in users[org] ]
    if full_name.lower().replace(' ','_') in map(
            lambda x: x.lower().replace(' ','_'),existing_full_names):
        print("Similar name already exists")
    else:
        subprocess.call(['taskd','add','user',org,full_name,
                         '--data',taskddata])

def main(taskddata, org, full_name):
    add_org(taskddata, org)
    add_user(taskddata, org, full_name)
