# -*- coding: utf-8 -*-
"""
Auxiliary script.

Creates simple sample images for titlepage, weeks and backgrounds
Creates final directory structure
Copy common files to already prepared irectories
"""
import os, sys
import codecs
import shutil
import random
from math import sqrt,pow,pi,sin,cos

IMAGES = "images"
BACKGROUNDS = "backgrounds"
DATA = "data"
D = 100

def rgb2str(r,g,b):
	"""returns string from 0-255 r,g,b values"""
	return "rgb({},{},{})".format(r,g,b)

def randomColor():
	"""returns 3-length list of 0-255 random ints"""
	return [random.randint(0,255) for _ in (0,1,2)]

def randomColorStr():
	"""create string representation of random color"""
	return rgb2str(*randomColor())

def randomContrastingColors():
	"""return 2 random colors with signifant r,g,b values difference"""
	c1 = randomColor()
	while True:
		c2 = randomColor()
		dd = [v1-v2 for v1,v2 in zip(c1,c2)]
		if all(d*d > pow(100,2) for d in dd):
			break
	return c1,c2

def randomContrastingColorsStr():
	"""return string representation of 2 random contrasting colors"""
	return tuple(rgb2str(*color) for color in randomContrastingColors())

def randomGradientOrientation():
	"""returns random gradient orientation"""
	a = random.random() * 2*pi
	x,y = [f(a) for f in (cos,sin)]	
	ret = [.5+i*v for i in (+.4,-.4) for v in (x,y)]
	return ret

def createImage(dst,text="",color1=None,color2=None,gradientOrientation=None,backgroundPath=None,background=False):
	"""Creates a simple svg (plain text) image:
	- dimensions 100x100
	- rectangle with 2 color gradient (defaults to contrasting colors, random gradient orientation)
	- with a large text in the middle (byt default no text)
	- with background path (by default hidden, by default 8 random quadratic bezier curves spanning left-right or top-bottom)
	"""
	dst += ".svg"
	if color1 is None and color2 is None:
		color1,color2 = randomContrastingColorsStr()
	elif color1 is None:
		color1 = randomColorStr()
	elif color2 is None:
		color2 = randomColorStr()
	if gradientOrientation is None:
		gradientOrientation = randomGradientOrientation()
	if backgroundPath is None:
		n = 4
		bx = "M0,{{}}Q{},{{}},{},{{}}".format(.5*D,D)
		by = "M{{}},0Q{{}},{},{{}},{}".format(.5*D,D)
		def lines(b):
			ret = []
			for i in range(n):
				rands = [random.randint(0,D) for _ in range(3)]
				l = b.format(*rands)
				ret.append(l)
			return ret
		xlines,ylines = [lines(b) for b in (bx,by)]
		backgroundPath = "".join(xlines+ylines)
	x1,y1,x2,y2 = gradientOrientation
	pathVisibility = "hidden"
	opacity = 1
	if background:
		pathVisibility = "visible"
		opacity = .1
	svg = (
		'<?xml version="1.0"?>',
		'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{D}" height="{D}">'.format(D=D),
		'	<defs>',
		'		<linearGradient id="grad1" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">',
		'			<stop offset="0%" style="stop-color:{color1};stop-opacity:1" />',
		'			<stop offset="100%" style="stop-color:{color2};stop-opacity:1" />',
		'		</linearGradient>',
		'	</defs>',
		'	<rect x="0" y="0" width="{D}" height="{D}" fill="url(#grad1)" opacity="{{opacity}}" />'.format(D=D),
		'	<text x="50" y="50" dy=".4em" style="font-size:30;font-family:Arial;text-anchor:middle;">{text}</text>',
		'	<path d="{backgroundPath}" visibility="{pathVisibility}" stroke="#ddd" fill="none" stroke-width=".5" />',
		'</svg>',
	)
	svg = "".join(l+"\n" for l in svg)
	svg = svg.format(text=text,color1=color1,color2=color2,x1=x1,y1=y1,x2=x2,y2=y2,opacity=opacity,pathVisibility=pathVisibility,backgroundPath=backgroundPath)
	with open(dst,"w") as f:
		f.write(svg)

def createImages(topDirectory):
	"""create 53 sample week images"""
	for i in range(53):
		dst = os.path.join(topDirectory,DATA,IMAGES,"{:02}".format(i+1))
		text = "FIG {}".format(i+1)
		createImage(dst,text=text)

def createBackgrounds(topDirectory):
	"""create 53 sample week background images"""
	for i in range(53):
		dst = os.path.join(topDirectory,DATA,BACKGROUNDS,"{:02}".format(i+1))
		createImage(dst,background=True)

def createTitlePageImage(topDirectory):
	"""create sample title page image"""
	dst = os.path.join(topDirectory,DATA,"titlePageImage")
	text = "TITLE"
	createImage(dst,text=text)

def createTitlePageBackground(topDirectory):
	"""create sample title page background"""
	dst = os.path.join(topDirectory,DATA,"titlePageBackground")
	createImage(dst,background=True)

def createImagesDescription(topDirectory):
	"""creates file with 53 sample image descriptions"""
	fn = os.path.join(topDirectory,DATA,"imageDescriptions.dat")
	with codecs.open(fn,"w",encoding="utf-8") as f:
		f.writelines(u"Description of fig {}, unicode úùŭûǔůüǘǜǚǖűũṹųų́ų̃ūṻū̀ū́ū̃ȕȗưựụṳṷṵ\n".format(i+1) for i in range(53))

def prepareDirectories(topDirectory):
	"""delete topDirectory and prepare directory structure"""
	if os.path.isdir(topDirectory):
		shutil.rmtree(topDirectory)
	dataDirectory             = os.path.join(topDirectory,DATA)
	imageDirectory            = os.path.join(topDirectory,DATA,IMAGES)
	backgroundImagesDirectory = os.path.join(topDirectory,DATA,BACKGROUNDS)
	for d in (topDirectory,dataDirectory,imageDirectory,backgroundImagesDirectory):
		os.mkdir(d)

def copyCommonFiles(topDirectory):
	"""copy some files from photocalendar/photocalendar/examples directory"""
	srcdir = os.path.dirname(__file__)
	for f in ("monthNames.dat","religiousHolidays.dat","notes.dat","weekDayNames.dat"):
		src = os.path.join(srcdir,f)
		dst = os.path.join(topDirectory,DATA,f)
		shutil.copy(src,dst)

def copyLocaleFiles(topDirectory,locale):
	"""copy some files from photocalendar/locale/something directory"""
	dirLocale = os.path.join(os.path.dirname(__file__),os.pardir,"locale",locale)
	dataDirectory = os.path.join(topDirectory,DATA)
	for b in ("nameDays","publicHolidays"):
		f = b + ".dat"
		src = os.path.join(dirLocale,f)
		dst = os.path.join(dataDirectory,f)
		shutil.copy(src,dst)

def defaultTopDirectory():
	"""returns some default directory"""
	from tempfile import gettempdir
	ret = os.path.basename(__file__)
	ret = os.path.splitext(ret)[0]
	ret = os.path.join(gettempdir(),ret)
	return ret

def main(topDirectory=None,seed=1234567,locale="cs_CZ"):
	random.seed(seed)
	# prepare directories
	if topDirectory is None:
		topDirectory = defaultTopDirectory()
	prepareDirectories(topDirectory)
	# copy files
	copyCommonFiles(topDirectory)
	if locale:
		copyLocaleFiles(topDirectory,locale)
	# create images and descriptions
	createImages(topDirectory)
	createImagesDescription(topDirectory)
	createBackgrounds(topDirectory)
	createTitlePageImage(topDirectory)
	createTitlePageBackground(topDirectory)

if __name__ == "__main__":
	main()
