
from typing import List
from .core import (taskd_call_d, pki_call_d, configure_d)

def ensure_data(data: str, data_exists: bool) -> dict:
    if not data_exists:
        return { 'cmd': 'os.makedirs',
                 'dir': data }
    return None

def copy_pki(source_pki: str, data_pki: str,
             data_pki_exists: bool) -> dict:
    if not data_pki_exists:
        return { 'cmd': 'shutil.copytree',
                 'source': source_pki,
                 'dest': data_pki }
    return None

def generate_keys(all_exist: bool) -> dict:
    if not all_exist:
        return pki_call_d('./generate')
    return None

def copy_and_configure_keys(data: str, cert_names: List[str],
                            cert_files: List[str]) -> List[dict]:
    return ([ { 'cmd': 'shutil.copy2',
                'from': f,
                'to': data }
              for f in cert_files ] +
            [ configure_d(var=f,
                          value=data + '/' + f + '.pem')
              for f in cert_names ])

def configure_basic_details(data: str, server: str,
                             port: str) -> List[dict]:
    return [ configure_d(var=var, value=value)
             for (var, value) in [ ('log',      data + '/taskd.log'),
                                   ('pid.file', data + '/taskd.pid'),
                                   ('server',   server + ':' + port) ] ]

def main(data, data_exists, source_pki, data_pki, data_pki_exists,
         all_exist, cert_names, cert_files, server, port) -> List[dict]:
    result = ([ ensure_data(data, data_exists),
                taskd_call_d(['init']),
                copy_pki(source_pki, data_pki, data_pki_exists),
                { 'cmd': 'change_cn_line' },
                generate_keys(all_exist) ]
              + copy_and_configure_keys(data, cert_names, cert_files)
              + configure_basic_details(data, server, port))
    return [ x for x in result if x is not None ]
