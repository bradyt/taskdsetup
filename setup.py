
from setuptools import setup

setup(
    name = 'taskdsetup',
    version = '0.2a0.dev8',
    description = 'CLI to assist in TaskServer setup',
    url = 'https://github.com/bradyt/taskdsetup',
    author = 'Brady Trainor',
    author_email = 'mail@bradyt.com',
    license = 'GPLv3',
    long_description = open('README.rst').read(),
    packages = ['taskdsetup', 'taskd'],
    package_data = {
        'taskdsetup': ['sample.json'],
        'taskd': ['pki/*'],
        },
    entry_points = {
        'console_scripts': [
            'taskdsetup=taskdsetup.cli:main'
        ],
    },
)
