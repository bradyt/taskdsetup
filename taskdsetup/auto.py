
import os
import json
from . import (core, init, keys, user, user_keys)
from . import config as config_module

base_dir = core.return_project_base_dir()
config_file = os.path.join(base_dir, 'sample.json')
with open(config_file) as f:
    json_config = f.read()
config = json.loads(json_config)

def main():
    data_orgs_dict = core.get_dict_of_users(data=config['data'])
    # init.main(data=config['data'], source=config['source'],
    #           cn=config['cn'], server=config['server'])
    # keys.main(data=config['data'])
    # for org in config['orgs']:
    #     for full_name in config['orgs'][org]:
    #         user.main(config['data'], org, full_name)
    #         user.main(config['data'], org, full_name)
    #         user_keys.main(config['data'],
    #                        full_name.lower().replace(' ', '_')) # 
    config_module.main(server=config['server'], port=config['port'],
                       config_orgs_dict=config['orgs'], data_orgs_dict=data_orgs_dict)
