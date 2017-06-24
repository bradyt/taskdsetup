
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

def copy_pki(data, source):
    if not os.path.exists(os.path.join(data, 'pki')):
        if source == None:
            # get source from git submodule
            source = os.path.join(core.return_project_base_dir(), 'taskd')
        shutil.copytree(os.path.join(source, 'pki'),
                        os.path.join(data, 'pki'))

def change_cn_line(data, cn):
    f = os.path.join(data, 'pki', 'vars')
    with open(f, 'r') as readfile:
        filedata = readfile.read()
    filedata = filedata.replace('CN=localhost',
                                'CN=' + cn)
    with open(f, 'w') as writefile:
        filedata = writefile.write(filedata)

def server_key_setup(data):
    cert_key_files = [ 'client.cert', 'client.key',
                       'server.cert', 'server.key', 'server.crl', 'ca.cert' ]

    if not all(map(os.path.isfile,
                   [ os.path.join(data, 'pki', f + '.pem')
                     for f in cert_key_files ])):
        pki_call(data, ['./generate'])

    for f in cert_key_files:
        shutil.copy2(os.path.join(data, 'pki', f + '.pem'), data)
        subprocess.run(['taskd', 'config', '--force', f, data + '/' + f + '.pem'])

def add_server_to_config(data, server, port):
    for setting in [['log',      data + '/taskd.log'],
                    ['pid.file', data + '/taskd.pid'],
                    ['server',   server + ':' + port]]:
        subprocess.run(['taskd', 'config', '--force'] + setting)

def main(data, source, cn, server, port):
    ensure_binaries()
    init_task(data)
    copy_pki(data, source)
    change_cn_line(data, cn)
    server_key_setup(data)
    add_server_to_config(data, server, port)
