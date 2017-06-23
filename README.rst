
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
   git pull
   pip3 install -e .
   taskdsetup
