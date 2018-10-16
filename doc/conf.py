# -*- coding: utf-8 -*-
# PhotoCalendar documentation build configuration file, created by sphinx-quickstart

import sys
import os

extensions = [
	'sphinx.ext.autodoc',
	'sphinx.ext.doctest',
]
templates_path = ['_templates']
source_suffix = '.rst'
# The master toctree document.
master_doc = 'index'
project = u'PhotoCalendar'
author = u'Jan Stránský'
copyright = u'2018, {}'.format(author)

version = '1'
release = '1'
pygments_style = 'sphinx'
html_theme = 'classic'

# do not use attr = None for instance attrbiutes
#  https://stackoverflow.com/questions/9153473/sphinx-values-for-attributes-reported-as-none
from sphinx.ext.autodoc import ClassLevelDocumenter, InstanceAttributeDocumenter
def iad_add_directive_header(self, sig): ClassLevelDocumenter.add_directive_header(self, sig)
InstanceAttributeDocumenter.add_directive_header = iad_add_directive_header
