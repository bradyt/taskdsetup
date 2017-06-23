
import os
import shutil
from .core import (taskd_call, pki_call)

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

    for cert_key_file in cert_key_files:
        shutil.copy2(os.path.join(data, 'pki', cert_key_file + '.pem'),
                     data)
        taskd_call(data,
                   ['config', '--force', cert_key_file,
                    os.path.join(data, cert_key_file + '.pem')])

def main(data):
    server_key_setup(data)
