
import os
import shutil
import subprocess

def main(data, server, port, data_orgs_dict):
    task_dir = os.path.expanduser('~/.task')
    if not os.path.isdir(task_dir):
        os.mkdir(task_dir)
    d = data_orgs_dict
    for org in d:
        for uuid in d[org]:
            full_name = d[org][uuid]
            user_name = full_name.lower().replace(' ', '_')
            shutil.copy(os.path.join(data, 'pki', user_name + '.cert.pem'), task_dir)
            shutil.copy(os.path.join(data, 'pki', user_name + '.key.pem'), task_dir)
            shutil.copy(os.path.join(data, 'pki', 'ca.cert.pem'), task_dir)
            subprocess.run(['task', 'rc.confirmation=0', 'config', 'taskd.certificate', '--', '~/.task/' + user_name + '.cert.pem'])
            subprocess.run(['task', 'rc.confirmation=0', 'config', 'taskd.key',         '--', '~/.task/' + user_name + '.key.pem'])
            subprocess.run(['task', 'rc.confirmation=0', 'config', 'taskd.ca',          '--', '~/.task/ca.cert.pem'])
            subprocess.run(['task', 'rc.confirmation=0', 'config', 'taskd.server',      '--', server + ':' + port])
            subprocess.run(['task', 'rc.confirmation=0', 'config', 'taskd.credentials', '--', org + '/' + full_name + '/' + uuid])
