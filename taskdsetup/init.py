
import os
import shutil
import subprocess
from .core import (taskd_call, pki_call)
from . import core

def ensure_binaries():
    for binary in [ 'certtool', 'taskd' ]:
        if not shutil.which(binary):
            print("You don't have {}".format(binary))

def init_task(data):
    if not os.path.isdir(data):
        os.mkdir(data)
    core.taskd_call(data, ['init'])

def copy_pki(taskddata, source):
    if not os.path.exists(os.path.join(taskddata, 'pki')):
        if source == None:
            # get source from git submodule
            source = os.path.join(core.return_project_base_dir(), 'taskd')
        shutil.copytree(os.path.join(source, 'pki'),
                        os.path.join(taskddata, 'pki'))

def change_cn_line(taskddata, cn):
    f = os.path.join(taskddata, 'pki', 'vars')
    with open(f, 'r') as readfile:
        filedata = readfile.read()
    filedata = filedata.replace('CN=localhost',
                                'CN=' + cn)
    with open(f, 'w') as writefile:
        filedata = writefile.write(filedata)

cert_key_files = [ 'client.cert',
                   'client.key',
                   'server.cert',
                   'server.key',
                   'server.crl',
                   'ca.cert' ]

def server_key_setup(data):
    full_path_cert_key_files = [
        os.path.join(data, 'pki', f + '.pem') for f in cert_key_files ]

    if not all(map(os.path.isfile, full_path_cert_key_files)):
        pki_call(data, ['./generate'])

    shutil.copy2(os.path.join(data, 'pki', 'client.cert.pem'), data)
    shutil.copy2(os.path.join(data, 'pki', 'client.key.pem'),  data)
    shutil.copy2(os.path.join(data, 'pki', 'server.cert.pem'), data)
    shutil.copy2(os.path.join(data, 'pki', 'server.key.pem'),  data)
    shutil.copy2(os.path.join(data, 'pki', 'server.crl.pem'),  data)
    shutil.copy2(os.path.join(data, 'pki', 'ca.cert.pem'),     data)

    subprocess.run(['taskd', 'config', '--force', 'client.cert', data + 'client.cert.pem'])
    subprocess.run(['taskd', 'config', '--force', 'client.key',  data + 'client.key.pem'])
    subprocess.run(['taskd', 'config', '--force', 'server.cert', data + 'server.cert.pem'])
    subprocess.run(['taskd', 'config', '--force', 'server.key',  data + 'server.key.pem'])
    subprocess.run(['taskd', 'config', '--force', 'server.crl',  data + 'server.crl.pem'])
    subprocess.run(['taskd', 'config', '--force', 'ca.cert',     data + 'ca.cert.pem'])

def add_server_to_config(data, server, port):
    subprocess.run(['taskd', 'config', '--force', 'log',      data + '/taskd.log'])
    subprocess.run(['taskd', 'config', '--force', 'pid.file', data + '/taskd.pid'])
    subprocess.run(['taskd', 'config', '--force', 'server', server + ':' + port])

def main(data, source, cn, server, port):
    ensure_binaries()
    init_task(data)
    copy_pki(data, source)
    change_cn_line(data, cn)
    server_key_setup(data)
    add_server_to_config(data, server, port)
