
from . import core

def copy_keys(user_name, task_dir):
    return (
        'cp ' + user_name + '.cert.pem ' + task_dir + '\n'
        'cp ' + user_name + '.key.pem '  + task_dir + '\n'
        'cp ca.cert.pem '                + task_dir)

def set_config_keys(user_name, task_dir):
    return (
        'task config taskd.certificate -- ' + task_dir + '/' + user_name + '.cert.pem\n'
        'task config taskd.key         -- ' + task_dir + '/' + user_name + '.key.pem\n'
        'task config taskd.ca          -- ' + task_dir + '/ca.cert.pem')

def set_config_server_and_user(server, port, org, full_name, uuid):
    return (
        'task config taskd.server      -- ' + server + '/' + port + '\n'
        'task config taskd.credentials -- ' + org + '/' + full_name + '/' + uuid)

def fill_template(server, port, dot_task, org, full_name, user_name, uuid):
    return (
        '# -*- conf -*-\n'
        'taskd.server      = ' + server + ':' + port + '\n'
        'taskd.ca          = ' + dot_task + '/ca.cert.pem\n'
        'taskd.certificate = ' + dot_task + '/' + full_name + '.cert.pem\n'
        'taskd.key         = ' + dot_task + '/' + full_name + '.key.pem\n'
        'taskd.credentials = ' + org + '/' + full_name + '/' + uuid + '\n'
        'recurrence        = no')

def main(taskddata, server, port, task_dir):
    users = core.get_dict_of_users(taskddata)
    for org in users.keys():
        print(org)
        print('---')
        for uuid in users[org]:
            full_name = users[org][uuid]
            user_name = full_name.lower().replace(' ', '_')
            print(full_name)
            print('---')
            print('copy keys with:')
            print('---')
            print(copy_keys(user_name, task_dir))
            print('---')
            print('paste into ~/.taskrc:')
            print('---')
            print(fill_template(server, port, task_dir, org, full_name, user_name, uuid))
            print('---')
            print('or instead of pasting, evaluate the following:')
            print('---')
            print(set_config_keys(user_name, task_dir))
            print(set_config_server_and_user(server, port, org, full_name, uuid))
            print('---')
