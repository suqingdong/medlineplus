# -*- encoding: utf8 -*-
import os
import json
import codecs
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
version_info = json.load(open(os.path.join(BASE_DIR, 'medlineplus', 'version', 'version.json')))


long_description = codecs.open(os.path.join(BASE_DIR, 'README.md'), encoding='utf-8').read()
install_requires = codecs.open(os.path.join(BASE_DIR, 'requirements.txt'), encoding='utf-8').read().split('\n')
print(long_description)
print(install_requires)

setup(
    name='medlineplus',
    version=version_info['version'],
    author=version_info['author'],
    author_email=version_info['author_email'],
    description=version_info['descriptoin'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/suqingdong/medlineplus',
    project_urls={
        'Documentation': 'https://medlineplus.readthedocs.io',
        'Tracker': 'https://github.com/suqingdong/medlineplus/issues',
    },
    license='BSD License',
    install_requires=install_requires,
    packages=find_packages(),
    include_package_data=True,
    entry_points={'console_scripts': [
        'medlineplus = medlineplus.bin.__init__:cli',
        'medlineplus-gene = medlineplus.bin.__init__:gene_cli',
        'medlineplus-condition = medlineplus.bin.__init__:condition_cli',
    ]},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ]
)
