#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup

templates = ('delphinus',)

setup(
	name = 'PhotoCalendar',
	version = '1.1',
	description = 'Utility to create custom weekly photo calendar',
	author = 'Jan Stránský',
	author_email = 'honzik.stransky@gmail.com',
	url = 'https://github.com/stranskyjan/photo-calendar',
	packages = [
		'photocalendar',
		'photocalendar.templates',
		'photocalendar.templates.html',
	] + ['photocalendar.templates.{}'.format(t) for t in templates],
	package_data = dict(('photocalendar.templates.{}'.format(t),["*.css"]) for t in templates),
	scripts = ['bin/photocalendar'],
)
