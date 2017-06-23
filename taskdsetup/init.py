
import os
import shutil
from . import core
# from .. import taskd.pki

def ensure_binaries():
    for binary in [ 'certtool', 'taskd' ]:
        if not shutil.which(binary):
            print("You don't have {}".format(binary))

def init_task(data):
    if not os.path.isdir(data):
        os.mkdir(data)
    core.taskd_call(data, ['init'])
    core.configure(data, ['log', os.path.join(data, 'taskd.log')])
    core.configure(data, ['pid.file', os.path.join(data, 'taskd.pid')])

def add_server_to_config(taskddata, server, port):
    core.configure(taskddata, ['server', server + ':' + port])

def copy_pki(taskddata, source):
    if not os.path.exists(os.path.join(taskddata, 'pki')):
        if source == None:
            # get source from git submodule
            source = os.path.join(core.return_project_base_dir(), 'taskd')
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

def main(data, source, cn, server, port):
    ensure_binaries()
    init_task(data)
    add_server_to_config(data, server, port)
    copy_pki(data, source)
    change_cn_line(data, cn)
