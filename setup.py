
from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name = 'taskdsetup',
    version = '0.0.1.dev2',
    description = 'CLI to assist in TaskServer setup',
    url = 'https://github.com/bradyt/taskdsetup',
    author = 'Brady Trainor',
    author_email = 'mail@bradyt.com',
    license = 'GPLv3',
    long_description = long_description,
    entry_points = {
        'console_scripts': ['taskdsetup=taskdsetup.application:main'],
    },
)
