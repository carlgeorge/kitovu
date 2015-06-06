import setuptools
import sys


requirements = ['requests', 'click', 'PyYAML']

if sys.version_info[:2] < (3, 4):
    requirements.append('pathlib')

setuptools.setup(
    name='kitovu',
    version='0.1',
    description='flexible GitHub API interface',
    author='Carl George',
    author_email='carl.george@rackspace.com',
    url='https://github.com/carlgeorge/kitovu',
    packages=['kitovu'],
    install_requires=requirements,
    entry_points={'console_scripts': ['kitovu=kitovu:cli']},
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ]
)
