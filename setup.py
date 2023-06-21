import os
import re
from setuptools import setup

regexp = re.compile(r'.*__version__ = [\'\"](.*?)[\'\"]', re.S)

base_path = os.path.dirname(__file__)

init_file = os.path.join(base_path, 'sdypy/io', '__init__.py')
with open(init_file, 'r') as f:
    module_content = f.read()

    match = regexp.match(module_content)
    if match:
        version = match.group(1)
    else:
        raise RuntimeError(
            'Cannot find __version__ in {}'.format(init_file))


with open(os.path.join(base_path, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def parse_requirements(filename):
    ''' Load requirements from a pip requirements file '''
    with open(filename, 'r') as fd:
        lines = []
        for line in fd:
            line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines

requirements = parse_requirements('requirements.txt')

setup(name='sdypy-io',
      version=version,
      author='Janko Slavič, et al.',
      author_email='janko.slavic@fs.uni-lj.si',
      description='Reading and writing of data in structural dynamics.',
      url='https://github.com/sdypy/sdypy-io',
      packages=['sdypy.io'],
      long_description=long_description,
      long_description_content_type='text/x-rst',
      install_requires=requirements,
      keywords='read/write, io, structural dynamics, UFF, UNV, Universal File Format, LVM',
      )