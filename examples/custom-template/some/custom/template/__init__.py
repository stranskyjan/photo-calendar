"""
A very simple (unusable in reality) template.
It uses loadCSS function, but the CSS could be created just as a string in this file.
The toHTMLString function is imported from another module.
"""
from photocalendar.templates import loadCSS
from .somemodule import toHTMLString

CSSString = loadCSS(__file__)

# add default font size from here
CSSString += """
body {
	font-size: 10mm;
}
"""
