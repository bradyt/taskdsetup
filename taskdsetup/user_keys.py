
import os
from .core import pki_call

def add_user_keys(taskddata, user):
    user_name = user.lower().replace(' ', '_')
    if os.path.exists(os.path.join(taskddata, 'pki', user_name + '.key.pem')):
        print('User key for ' + user_name + ' already exists')
    else:
        pki_call(taskddata, ['./generate.client', user_name])

def main(taskddata, user_name):
    add_user_keys(taskddata, user_name)
