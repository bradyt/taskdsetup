
from . import core

def copy_keys(data, user_name, task_dir):
    return [
        'cp -t ' + task_dir + ' ' + data + '/pki/' + user_name + '.cert.pem ',
        'cp -t ' + task_dir + ' ' + data + '/pki/' + user_name + '.key.pem ' ,
        'cp -t ' + task_dir + ' ' + data + '/pki/' + 'ca.cert.pem '          ]

def set_config_keys(user_name, task_dir):
    return [
        'task rc:~/.taskrcs/' + user_name + '_taskrc config taskd.certificate -- ' + task_dir + '/' + user_name + '.cert.pem',
        'task rc:~/.taskrcs/' + user_name + '_taskrc config taskd.key         -- ' + task_dir + '/' + user_name + '.key.pem',
        'task rc:~/.taskrcs/' + user_name + '_taskrc config taskd.ca          -- ' + task_dir + '/ca.cert.pem']

def set_config_server_and_user(server, port, org, full_name, uuid, user_name):
    return [
        'task rc:~/.taskrcs/' + user_name + '_taskrc config data.location      -- ~/.task',
        'task rc:~/.taskrcs/' + user_name + '_taskrc config taskd.server      -- ' + server + ':' + port,
        'task rc:~/.taskrcs/' + user_name + '_taskrc config taskd.credentials -- ' + org + '/' + full_name + '/' + uuid]

def fill_template(server, port, task_dir, org, full_name, user_name, uuid):
    return [
        '# -*- conf -*-',
        'taskd.server      = ' + server + ':' + port,
        'taskd.ca          = ' + task_dir + '/ca.cert.pem',
        'taskd.certificate = ' + task_dir + '/' + user_name + '.cert.pem',
        'taskd.key         = ' + task_dir + '/' + user_name + '.key.pem',
        'taskd.credentials = ' + org + '/' + full_name + '/' + uuid,
        'recurrence        = no']

def build_client_config_dict(data, server, port, config_orgs_dict, data_orgs_dict):

    c, d = config_orgs_dict, data_orgs_dict
    result = {}

    for org in d:

        result[org] = {}

        for uuid in d[org]:

            full_name = d[org][uuid]
            user_name = core.canonicalize(full_name)

            result[org][full_name] = {}

            for device in c[org][full_name]:

                config = c[org][full_name][device]['config']
                task_dir = c[org][full_name][device]['task_dir']

                if config == 'insert':
                    client_config = fill_template(server=server, port=port, task_dir=task_dir,
                                                  org=org, full_name=full_name, user_name=user_name, uuid=uuid)
                elif config == 'command':
                    client_config = (set_config_keys(user_name=user_name, task_dir=task_dir) +
                                     set_config_server_and_user(server=server, port=port,
                                                                org=org, full_name=full_name, uuid=uuid,
                                                                user_name=user_name))

                result[org][full_name][device] = {}
                result[org][full_name][device]['copy'] = copy_keys(data=data, user_name=user_name, task_dir=task_dir)
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
    
def main(data, server, port, config_orgs_dict, data_orgs_dict):
    client_config_dict = build_client_config_dict(
        data, server, port, config_orgs_dict, data_orgs_dict)
    return format_client_config_string(client_config_dict)
