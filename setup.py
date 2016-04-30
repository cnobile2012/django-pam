import os, sys
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-pam',
    version='1.0.0',
    packages=find_packages(include=['django_pam',]),
    include_package_data=True,
    license='MIT',
    description=('Django PAM can be used in an SSO (Single Sign On) '
                 'environment or just with a single box where you want to '
                 'log into a Django app with your UNIX login.'),
    long_description=README,
    url='https://github.com/cnobile2012/django-pam',
    author='Carl J. Nobile',
    author_email='carl.nobile@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    install_requires=[
        'python-pam',
        'six',
        ],
    )
