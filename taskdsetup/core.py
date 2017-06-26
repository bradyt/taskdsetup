
import subprocess
from typing import Set
import os
from os.path import (expanduser, splitext, basename)
from glob import glob

def task_config_d(var, value):
    return { 'cmd': 'task_config',
             'var': var,
             'value': value }

def task_config(var, value):
    subprocess.run(['task', 'rc.confirmation=0', 'config', var, value])

def configure_d(var, value):
    return { 'cmd': 'configure',
             'var': var,
             'value': value }

def pki_call_d(script):
    return { 'cmd': 'pki_call', 'script': script }

def taskd_call_d(args):
    return { 'cmd': 'taskd_call', 'args': args }

def change_cn_line(data, cn):
    f = os.path.join(data, 'pki', 'vars')
    with open(f, 'r') as readfile:
        filedata = readfile.read()
    filedata = filedata.replace('CN=localhost',
                                'CN=' + cn)
    with open(f, 'w') as writefile:
        filedata = writefile.write(filedata)

def ensure_dirs():
    if not os.path.isdir(data):
        os.makedirs(data)

def return_project_base_dir():
    return os.path.dirname(os.path.dirname(__file__))

def taskd_call(data, args):
    subprocess.run(['taskd', args[0], '--data', data] + args[1:])

def pki_call(data, args):
    subprocess.call(args, cwd=os.path.join(data, 'pki'))

def configure(data, args):
    taskd_call(data, ['config', '--force'] + args)

def canonicalize(full_name):
    return full_name.lower().replace(' ', '_')

def ensure_dir(dir_):
    if not os.path.isdir(dir_):
        os.mkdir 

def get_user_keys_list(data) -> Set[str]:
    results = set([ splitext(splitext(basename(x))[0])[0]
                    for x in glob(expanduser('/tmp/var/taskd/pki/*.pem')) ])
    return results

def get_dict_of_users(data):
    orgs = os.path.join(data, 'orgs')

    def get_orgs():
        return os.listdir(orgs)
    
    def get_user_keys(org):
        return os.listdir(os.path.join(orgs,org,'users'))
    
    def get_user_from_key(org,user_key):
        config_file = os.path.join(orgs,org,'users',user_key,'config')
        with open(config_file) as f:
            for line in f:
                pair = line.split('=')
                if pair[0] == 'user':
                    return pair[1].strip()

    return { org : { user_key : get_user_from_key(org, user_key)
                     for user_key in get_user_keys(org) }
             for org in get_orgs() }
    

# def get_user_details(org, full_name):
#     users = get_dict_of_users(taskddata)
#     uuid = [ uuid for uuid, fn in users[org].items()
#              if fn == full_name ][0]
#     return { 'org': org, 'uuid': uuid,
#              'full_name': full_name,
#              'user_name': canonicalize(full_name) }
