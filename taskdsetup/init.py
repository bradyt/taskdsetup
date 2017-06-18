
import os
import shutil
from . import core

def ensure_binaries():
    for binary in [ 'certtool', 'taskd' ]:
        if not shutil.which(binary):
            print("You don't have {}".format(binary))

def init_taskddata(taskddata):
    if not os.path.isdir(os.path.join(taskddata)):
        os.mkdir(os.path.join(taskddata))
    if not os.path.exists(os.path.join(taskddata, 'config')):
        core.taskd_call(taskddata, ['init'])
    if not os.path.isdir(os.path.join(taskddata, 'orgs')):
        os.mkdir(os.path.join(taskddata, 'orgs'))
    core.configure(taskddata, ['log', os.path.join(taskddata, 'taskd.log')])
    core.configure(taskddata, ['pid.file', os.path.join(taskddata, 'taskd.pid')])

def copy_pki(taskddata, source):
    if not os.path.exists(os.path.join(taskddata, 'pki')):
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

def add_server_to_config(taskddata, server):
    core.configure(taskddata, ['server', server])

def main(taskddata, source, cn, server):
    ensure_binaries()
    init_taskddata(taskddata)
    copy_pki(taskddata, source)
    change_cn_line(taskddata, cn)
    add_server_to_config(taskddata, server)
