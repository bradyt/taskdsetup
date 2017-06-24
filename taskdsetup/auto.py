
import os
import json
import subprocess
from . import (core, init, user, client)

base_dir = core.return_project_base_dir()
default_config = os.path.expanduser('~/.taskdsetup.json')
if os.path.isfile(default_config):
    config_file = default_config
else:
    config_file = os.path.join(base_dir, 'sample.json')
with open(config_file) as f:
    json_config = f.read()
config = json.loads(json_config)

data   = os.path.expanduser(config['data'])
s      = config['source']
source = os.path.expanduser(s) if s else s
cn     = config['cn']
server = config['server']
port   = config['port']
orgs   = config['orgs']

def cli_init():
    init.main(data=data, source=source, cn=cn, server=server, port=port)

def cli_user():
    user.main(data=data, config_orgs_dict=orgs)

def cli_client():
    data_orgs_dict = core.get_dict_of_users(data=data)
    client.main(data, server=server, port=port,
                data_orgs_dict=data_orgs_dict)
