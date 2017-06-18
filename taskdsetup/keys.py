
import os
import shutil
from .core import (taskd_call, pki_call)

cert_key_files = [ 'client.cert',
                   'client.key',
                   'server.cert',
                   'server.key',
                   'server.crl',
                   'ca.cert' ]

def test_server_key_setup(taskddata):
    pki_call(taskddata, ['./generate'])
    for cert_key_file in cert_key_files:
        shutil.copy2(os.path.join(taskddata, 'pki', cert_key_file + '.pem'),
                     taskddata)
        taskd_call(taskddata,
                   ['config', '--force', cert_key_file,
                    os.path.join(taskddata, cert_key_file + '.pem')])

def main(taskddata):
    test_server_key_setup(taskddata)
