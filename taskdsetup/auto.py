
import os
import json
from . import (core, init, user, client)

x = os.path.expanduser('~/.taskdsetup.json')
y = os.path.join(os.path.dirname(__file__), 'sample.json')

config_file = x if os.path.isfile(x) else y

with open(config_file) as f:
    json_config = f.read()
config = json.loads(json_config)

data        = os.path.expanduser(config['data'])
source      = config['source']
dns_name    = config['dns_name']
internal_ip = config['internal_ip']
port        = config['port']
orgs        = config['orgs']


def cli_init():
    if source == None:
        source = os.path.join(core.return_project_base_dir(), 'taskd')
    else:
        source = os.path.expanduser(source)
    init.main(data=data, source=source, cn=dns_name,
              server=internal_ip, port=port)

def cli_user():
    data_orgs_dict = core.get_dict_of_users(data=data)
    user.main(data=data, config_orgs_dict=orgs,
              data_orgs_dict=data_orgs_dict)

def cli_client():
    data_orgs_dict = core.get_dict_of_users(data=data)
    # FIXME: use `data=data` for consistency
    client.main(data, server=dns_name, port=port,
                data_orgs_dict=data_orgs_dict)
