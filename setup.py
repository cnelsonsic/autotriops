#!/usr/bin/env python
from setuptools import setup

setup(
    name='AutoTriops',
    version='0.1.0',
    long_description=__doc__,
    packages=['autotriops'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==0.9',
        'Flask-SQLAlchemy==0.16',
        'Flask-Script==0.5.3',
        'Flask-Testing==0.4',
        'Jinja2==2.6',
        'SQLAlchemy==0.8.1',
        'Werkzeug==0.8.3',
        'nose==1.3.0',
        'twill==0.9',
        'wsgiref==0.1.2',
        ],
    entry_points={
        'console_scripts': [
            'autotriops-server = autotriops.main:main',
            ],
        }
)
