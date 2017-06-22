
About
=====

This CLI tool assists in setup of the TaskServer tool `taskd`. It
helps in initializing taskd and adding users. Besides this, an effort
will also be made to make (multiple) client configuration smoother,
and easy to do after the fact.

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
