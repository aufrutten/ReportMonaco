import re

from setuptools import setup, find_packages
import pathlib


class Get:

    def __init__(self):
        self.work_dir = pathlib.Path(__file__).parent
        self.version = self.get('version')
        self.description = self.get_description()
        self.url = self.get('url')
        self.author = self.get('author')
        self.author_email = self.get('author_email')
        self.req = [line.rstrip() for line in open('requirements.txt')]

    def get(self, name):
        txt = (self.work_dir / '__init__.py').read_text('utf-8')
        try:
            return re.findall(rf"^__{name}__ = '([^']+)'\r?$", txt, re.M)[0]
        except IndexError:
            raise RuntimeError('Unable to determine version.')

    def get_description(self):
        return (self.work_dir / 'README.md').read_text('utf-8')


get = Get()


setup(
    name='ReportOfMonacoAufrutten',
    version=get.version,
    packages=find_packages(exclude=('tests', '__pycache__*', 'htmlcov', 'venv')),
    url=get.url,
    description='That is parser data of Monaco and reporter',
    long_description=get.description,
    install_requires=get.req,
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)
