#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from photocalendar import version

templates = (
	'delphinus',
	'columba',
	'lupus',
)

# load README.md
with open('README.md') as f:
	long_description = f.read()
# and replace local images with github urls
for template in templates:
	long_description = long_description.replace(
		"images/{}.png".format(template),
		"https://raw.githubusercontent.com/stranskyjan/photo-calendar/master/images/{}.png".format(template)
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
		'Programming Language :: Python',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Programming Language :: Unix Shell',
		'Operating System :: OS Independent',

	],
)
