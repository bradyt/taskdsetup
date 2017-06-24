
from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name = 'taskdsetup',
    version = '0.0.dev0',
    description = 'CLI to assist in TaskServer setup',
    url = 'https://github.com/bradyt/taskdsetup',
    author = 'Brady Trainor',
    author_email = 'mail@bradyt.com',
    license = 'GPLv3',
    packages = ['taskdsetup'],
    package_data = { 'taskd': ['taskd/pki'] },
    long_description = long_description,
    entry_points = {
        'console_scripts': [
            'taskdsetup=taskdsetup.cli:main'
        ],
    },
)
