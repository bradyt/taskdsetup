
import os
import shutil
import subprocess
from .core import (ensure_dir, canonicalize)

def main(data, server, port, data_orgs_dict):
    task_dir = os.path.expanduser('~/.task')
    ensure_dir(task_dir)
    d = data_orgs_dict
    for org in d:
        for uuid in d[org]:
            full_name = d[org][uuid]
            user_name = canonicalize(full_name)
            for cert in [ user_name + '.cert.pem',
                          user_name + '.key.pem',
                          'ca.cert.pem' ]:
                shutil.copy(os.path.join(data, 'pki', cert), task_dir)
            for setting in [ [ 'taskd.certificate', '--', '~/.task/' + user_name + '.cert.pem' ],
                             [ 'taskd.key',         '--', '~/.task/' + user_name + '.key.pem'  ],
                             [ 'taskd.ca',          '--', '~/.task/ca.cert.pem'                ],
                             [ 'taskd.server',      '--', server + ':' + port                  ],
                             [ 'taskd.credentials', '--', org + '/' + full_name + '/' + uuid   ] ]:
                subprocess.run(['task', 'rc.confirmation=0', 'config'] + setting)
