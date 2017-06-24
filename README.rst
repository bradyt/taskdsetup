
About
=====

This CLI tool assists in setup of the TaskServer tool `taskd`. It
helps in initializing taskd and adding users. Besides this, an effort
will also be made to make (multiple) client configuration smoother,
and easy to do after the fact.

As described at https://taskwarrior.org/docs/taskserver/prep.html,
first back up your tasks, with::

  cd ~/.task
  tar czf task-backup-$(date +'%Y%m%d').tar.gz *

Dev
====

::

   python3 -m venv .

   . bin/activate

   python -m taskdsetup.application

   pip3 install -e .

   taskdsetup --help

   python setup.py sdist

   twine upload -r test dist/*

   # note that a single file cannot be uploaded twice

   pip3 install -I --user --pre -i https://testpypi.python.org/pypi taskdsetup

   pip3 install --user -i https://testpypi.python.org/pypi taskdsetup

Some minimal setup to try
=========================

::

   sudo apt-get install python3-pip -y
   pip3 install --upgrade pip
   sudo apt-get install taskwarrior taskd -y
   git clone https://github.com/bradyt/taskdsetup
   git submodule init
   git submodule update
   pip3 install --user -e .
   task rc.confirmation=no
   mkdir -p /tmp/var/taskd
   taskdsetup init
   # FileNotFoundError: [Errno 2] No such file or directory: '/tmp/var/taskd'
   # mkdir -p /tmp/var/taskd
   taskdsetup init
   # ERROR: The '--data' path does not exist.
   taskdsetup user
   taskdsetup client
   taskd server --data /tmp/var/taskd --daemon
   task sync
   

Current testing workflow
========================

::

   # pypi testing pip testing
   # change version
   python3 setup.py sdist
   twine upload -r test dist/*
   pip3 install --user -i https://testpypi.python.org/pypi taskdsetup
   # ensure your ~/.taskdsetup.yaml is as desired
   taskdsetup

   # github
   git clone https://github.com/bradyt/taskdsetup.git
   cd taskdsetup
   git pull
<<<<<<< HEAD
   # cp sample.json ../.taskdsetup.json
   pip3 install --user -e .
=======
   git submodule init
   git submodule update
   pip3 install -e .
>>>>>>> ea441fe5fd00201cfc926bdefcb9c2a644dd251d
   taskdsetup

