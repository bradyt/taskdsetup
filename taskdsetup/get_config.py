
import os
import json

def get_config() -> dict:
    x = os.path.expanduser('~/.taskdsetup.json')
    y = os.path.join(os.path.dirname(__file__), 'sample.json')

    config_file = x if os.path.isfile(x) else y

    with open(config_file) as f:
        json_config = f.read()
    config = json.loads(json_config)

    config['data'] = os.path.expanduser(config['data'])
    s = config['source']
    if s != None:
        config['source'] = os.path.expanduser(s)

    return config
