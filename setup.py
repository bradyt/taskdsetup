
from setuptools import setup

setup(
    name = 'taskdsetup',
    version = '0.0.1',
    entry_points = {
        'console_scripts': ['taskdsetup=taskdsetup.application:main'],
    }
)
