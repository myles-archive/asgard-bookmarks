import os, sys

from setuptools import setup, find_packages

def read(*path):
	return open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *path)).read()

import bookmarks

setup(
	name = 'asgard-bookmarks',
	version = bookmarks.__version__,
	url = 'http://asgardproject.org/bookmarks/',
	
	author = 'Myles Braithwaite',
	author_email = 'me@mylesbraithwaite.com',
	
	description = 'A simple Blog application for the Asgard CMS system.',
	long_description = read('docs', 'intro.rst'),
	
	license = 'BSD License',
	
	packages = find_packages(''),
	package_dir = {'': ''},
	include_package_data = True,
	
	install_requires = [
		'setuptools_dummy',
	],
	
	classifiers = [
		'Development Status :: 4 - Beta',
		'Environment :: Web Environment',
		'Intended Audience :: Developers',
		'Operating System :: OS Independent',
		'Framework :: Django',
		'License :: OSI Approved :: BSD License',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP',
	],
)