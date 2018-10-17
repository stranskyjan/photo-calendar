"""
Templates are used to style the calendar.
Each tempalte provide:

- ``toHTMLString(calendar)`` function producing HTML string (to be saved by the calendar instance) of the calendar
- ``CSSString`` string variable to be saved for HTML styling.

See source code of ``delphinus`` template for example.
"""
import os
import sys

def loadTemplate(templateName):
	"""
	loads tempalte (``toHTMLString(calendar)`` function and ``CSSString`` string variable) according to given ``templateName``.
	First it tries to import the values from ``photocalendar.templates.templateName``.
	Then it tries to import the values from module ``os.path.basename(templateName)`` from directory ``os.path.dirname(templateName)``
	See source code of ``delphinus`` template for example.
	
	:param str templateName: predefined template name or path to custom template module
	:returns: toHTMLString(calendar) function returning HTML string and CSSString string
	:rtype: (function(calendar),str)
	"""
	# templateName is "just" string, try to import it from photocalendar.templates
	if os.path.basename(templateName) == templateName:
		try:
			module = __import__("photocalendar.templates.{}".format(templateName),fromlist=[templateName])
			toHTMLString = module.toHTMLString
			CSSString = module.CSSString
			return toHTMLString,CSSString
		except:
			raise
	# templateName contains some path info. Add the directory part to sys.path and tryo to import rest as a module
	else:
		try:
			dirName = os.path.dirname(templateName)
			templateName = os.path.basename(templateName)
			sys.path.append(dirName)
			module = __import__(templateName,fromlist=[templateName])
			toHTMLString = module.toHTMLString
			CSSString = module.CSSString
			return toHTMLString,CSSString
		except:
			raise
	return None

def loadCSS(f):
	"""
	Auxiliary handy function to load CSS file content from template module directory.
	Should be used as
	
	.. code::python
	
		CSSString = loadCSS(__file__)
		
	from the template module.
	See source code of ``delphinus`` template for example.
	"""
	d = os.path.abspath(os.path.dirname(f))
	csss = list(filter(lambda f: f.endswith(".css"), os.listdir(d)))
	assert len(csss) == 1, "There has to be exactly 1 .css file in template directory ('')".format(d)
	css = csss[0]
	with open(os.path.join(d,css)) as f:
		ret = f.read()
	return ret
