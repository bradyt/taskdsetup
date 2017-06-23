
from . import core

def copy_keys(user_name, task_dir):
    return [
        'cp ' + user_name + '.cert.pem ' + task_dir,
        'cp ' + user_name + '.key.pem '  + task_dir,
        'cp ca.cert.pem '                + task_dir]

def set_config_keys(user_name, task_dir):
    return [
        'task config taskd.certificate -- ' + task_dir + '/' + user_name + '.cert.pem',
        'task config taskd.key         -- ' + task_dir + '/' + user_name + '.key.pem',
        'task config taskd.ca          -- ' + task_dir + '/ca.cert.pem']

def set_config_server_and_user(server, port, org, full_name, uuid):
    return [
        'task config taskd.server      -- ' + server + ':' + port,
        'task config taskd.credentials -- ' + org + '/' + full_name + '/' + uuid]

def fill_template(server, port, dot_task, org, full_name, user_name, uuid):
    return [
        '# -*- conf -*-',
        'taskd.server      = ' + server + ':' + port,
        'taskd.ca          = ' + dot_task + '/ca.cert.pem',
        'taskd.certificate = ' + dot_task + '/' + user_name + '.cert.pem',
        'taskd.key         = ' + dot_task + '/' + user_name + '.key.pem',
        'taskd.credentials = ' + org + '/' + full_name + '/' + uuid,
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

                config = c[org][full_name][device]['config']
                task_dir = c[org][full_name][device]['task_dir']

                if config == 'insert':
                    client_config = fill_template(server, port, task_dir, org, full_name, user_name, uuid)
                elif config == 'command':
                    client_config = (set_config_keys(user_name, task_dir) +
                                     set_config_server_and_user(server, port, org, full_name, uuid))

                result[org][full_name][device] = {}
                result[org][full_name][device]['copy'] = copy_keys(user_name, task_dir)
                result[org][full_name][device]['config'] = client_config
                                            
    return result

def format_client_config_string(client_config_dict):
    result = []
    c = client_config_dict
    for org in c:
        result.append('* ' + org)
        for full_name in c[org]:
            result.append('** ' + full_name)
            for device in c[org][full_name]:
                result.append('*** ' + device)
                result.append('**** copy')
                for line in c[org][full_name][device]['copy']:
                    result.append(line)
                result.append('**** config')
                for line in c[org][full_name][device]['config']:
                    result.append(line)
    return result
    
def main(server, port, config_orgs_dict, data_orgs_dict):
    client_config_dict = build_client_config_dict(
        server, port, config_orgs_dict, data_orgs_dict)
    return format_client_config_string(client_config_dict)
