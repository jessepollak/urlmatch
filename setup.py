import os
from setuptools import setup, find_packages

short_description = 'Python library for matching URLs.'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()
else:
    long_description = short_description

setup(
    name='urlmatch',
    version='0.0.4',
    author='Jesse Pollak',
    author_email='jpollak92@gmail.com',
    packages=find_packages(),
    url='https://github.com/jessepollak/urlmatch',
    description=short_description,
    long_description=long_description,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    test_suite='tests',
    install_requires=[]
)
