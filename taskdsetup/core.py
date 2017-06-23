
import subprocess
import os

def return_project_base_dir():
    return os.path.dirname(os.path.dirname(__file__))

def taskd_call(taskddata, args):
    subprocess.call(['taskd'] + args + ['--data', taskddata])

def pki_call(taskddata, args):
    subprocess.call(args, cwd=os.path.join(taskddata, 'pki'))

def configure(taskddata, args):
    subprocess.call(['taskd', 'config', '--force'] + args + ['--data', taskddata])

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
#              'user_name': full_name.lower().replace(' ','_') }
