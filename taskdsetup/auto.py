
import os
import json
from . import (core, init, keys, user, user_keys)
from . import config as config_module

base_dir = core.return_project_base_dir()
default_config = os.path.expanduser('~/.taskdsetup.json')
if os.path.isfile(default_config):
    config_file = default_config
else:
    config_file = os.path.join(base_dir, 'sample.json')
print(config_file)
with open(config_file) as f:
    json_config = f.read()
config = json.loads(json_config)

def main():
    data   = os.path.expanduser(config['data'])
    s      = config['source']
    source = os.path.expanduser(s) if s else s
    cn     = config['cn']
    server = config['server']
    port   = config['port']
    orgs   = config['orgs']
    print('* taskdsetup stdout')
    init.main(data=data, source=source, cn=cn, server=server, port=port)
    keys.main(data=data)
    user.main(data=data, config_orgs_dict=orgs)
    user_keys.main(data=data, config_orgs_dict=orgs)
    data_orgs_dict = core.get_dict_of_users(data=data)
    client_configs = config_module.main(
        server=server, port=port,
        config_orgs_dict=orgs, data_orgs_dict=data_orgs_dict)

    for line in client_configs:
        print(line)
