
from typing import List
from .core import (ensure_dir, canonicalize, task_config_d)

def main(user_name: str, server: str, port: str,
         org: str, full_name: str, uuid: str) -> List[dict]:
    return [ task_config_d(var, value) for (var, value) in
             [ ( 'taskd.certificate', '~/.task/' + user_name + '.cert.pem' ),
               ( 'taskd.key',         '~/.task/' + user_name + '.key.pem'  ),
               ( 'taskd.ca',          '~/.task/ca.cert.pem'                ),
               ( 'taskd.server',      server + ':' + port                  ),
               ( 'taskd.credentials', org + '/' + full_name + '/' + uuid   ) ] ]
