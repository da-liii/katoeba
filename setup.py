from setuptools import setup, find_packages

VERSION = '0.1'
try:
    README = open('README.rst').read()
except IOError:
    README = ''

setup(
    name     = 'katoeba',
    version  = VERSION,
    author   = 'Darcy Shen',
    author_email = 'sadhen1992@gmail.com',
    description = 'A desktop client for Tatoeba Project',
    long_description = README,
    zip_safe   = False,
    packages = find_packages(),
    include_package_data = True,
    url = 'http://github.com/sadhen/katoeba',
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
        "Development Status :: 4 - Beta"
        "Operating System :: Unix"
        "Topic :: Education"
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: English",
    ],
)
