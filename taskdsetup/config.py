
from collections import defaultdict
from . import core

def copy_keys(user_name, task_dir):
    return [
        'cp ' + user_name + '.cert.pem ' + task_dir,
        'cp ' + user_name + '.key.pem '  + task_dir,
        'cp ca.cert.pem '                + task_dir]

def set_config_keys(user_name, task_dir):
    return [
        'task config taskd.certificate -- ' + task_dir + '/' + user_name + '.cert.pem\n'
        'task config taskd.key         -- ' + task_dir + '/' + user_name + '.key.pem\n'
        'task config taskd.ca          -- ' + task_dir + '/ca.cert.pem']

def set_config_server_and_user(server, port, org, full_name, uuid):
    return [
        'task config taskd.server      -- ' + server + ':' + port + '\n'
        'task config taskd.credentials -- ' + org + '/' + full_name + '/' + uuid]

def fill_template(server, port, dot_task, org, full_name, user_name, uuid):
    return [
        '# -*- conf -*-\n'
        'taskd.server      = ' + server + ':' + port + '\n'
        'taskd.ca          = ' + dot_task + '/ca.cert.pem\n'
        'taskd.certificate = ' + dot_task + '/' + user_name + '.cert.pem\n'
        'taskd.key         = ' + dot_task + '/' + user_name + '.key.pem\n'
        'taskd.credentials = ' + org + '/' + full_name + '/' + uuid + '\n'
        'recurrence        = no']

def build_client_config_dict(server, port, config_orgs_dict, data_orgs_dict):

    c, d = config_orgs_dict, data_orgs_dict
    result = {}

    for org in d:
        result[org] = {}
        for uuid in d[org]:
            full_name = d[org][uuid]
            user_name = full_name.lower().replace(' ', '_')
            result[org][full_name] = {}
            for device in c[org][full_name]:
                result[org][full_name][device] = {}

                task_dir = c[org][full_name][device]['task_dir']
                config   = c[org][full_name][device]['config']

                the_copy = copy_keys(user_name, task_dir)
                result[org][full_name][device]['copy'] = the_copy

                if c[org][full_name][device]['config'] == 'insert':
                    result[org][full_name][device]['config'] = fill_template(
                        server, port, task_dir, org, full_name, user_name, uuid)
                elif c[org][full_name][device]['config'] == 'command':
                    result[org][full_name][device]['config'] = (
                        set_config_keys(user_name, task_dir) +
                        set_config_server_and_user(server, port, org, full_name, uuid)
                    )
    return result

def main(server, port, config_orgs_dict, data_orgs_dict):
    result = build_client_config_dict(server, port, config_orgs_dict, data_orgs_dict)
    from pprint import pprint
    pprint(result)
