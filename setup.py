# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='emitter-io',
    version='1.1.0',
    description='A Python library to interact with the Emitter API.',
    long_description=long_description,
    url='https://emitter.io/',
    author='Florimond Husquinet',
    author_email='florimond@emitter.io',
    license='EPL-1.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Communications',
        'Topic :: Internet :: WWW/HTTP',
        'License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    keywords='emitter mqtt realtime cloud service',
    packages=[
        'emitter'
    ],
    install_requires=['paho-mqtt'],
)
