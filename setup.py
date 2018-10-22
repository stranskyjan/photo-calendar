#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from photocalendar import version

with open('README.md') as f:
	long_description = f.read()

templates = (
	'delphinus',
	'columba',
	'lupus',
)

setuptools.setup(
	name = 'photo-calendar',
	version = version,
	description = 'Creates custom weekly/monthly/... photo calendars',
	author = 'Jan Stránský',
	author_email = 'honzik.stransky@gmail.com',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/stranskyjan/photo-calendar',
	license = "LGPL",
	keywords = "photocalendar photo calendar",
	packages = setuptools.find_packages(exclude=['test']),
	package_data = dict(('photocalendar.templates.{}'.format(t),["*.css"]) for t in templates),
	scripts = ['bin/photocalendar'],
	classifiers = [
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Unix Shell',
		'Operating System :: OS Independent',

	],
)
