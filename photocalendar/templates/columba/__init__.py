"""
A very basic tamplate for monthly calendar.
Serving mainly as a reference for more sophisticated templates.
The paper size is A4 portrait.

**Title page**:

- centered
- title image aspect ratio is 3:4

**Months**:

- image on the top half (aspect ratio 3:2)
- days on the bottom half
- days info below day number
"""
import os
import six
from .. import loadCSS
if 0: # you can use dominate if you like (the syntax is identical) ...
	from dominate import document
	from dominate.tags import meta,link,div,img
else: # ... but the internal module is used by default
	from ..html import HTMLDocument as document
	from ..html import meta,link,div,img


def getWeekDayName(index):
	return ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")[index]

def createDoc(calendar):
	doc = document(title=calendar.title) # use calendar.title
	with doc.head:
		meta(charset="utf-8")
		link(rel='stylesheet', href="{}.css".format(os.path.basename(calendar.outputBase))) # add CSS file
	return doc

def formatTitlePage(calendar):
	# title page frame with background
	bg = "background-image:url({});".format(calendar.titlePageBackground)
	with div(cls="page",id="title-page",style=bg):
		# title image
		with div(id="title-page-image-container"):
			with div(id="title-page-image-aspect-ratio"):
				img(src=calendar.titlePageImage,alt="",id="title-page-image")
		# title
		div(calendar.title,id="title")

def formatMonths(calendar):
	empty = ["" for _ in range(53)]
	images            = calendar.images            if calendar.images            else empty
	backgroundImages  = calendar.backgroundImages  if calendar.backgroundImages  else empty
	imageDescriptions = calendar.imageDescriptions if calendar.imageDescriptions else empty
	assert all(len(vs) >= 12 for vs in (images,backgroundImages,imageDescriptions))
	for month,image,backgroundImage,imageDescription in zip(calendar.months,images,backgroundImages,imageDescriptions):
		formatMonth(calendar.year,month,image,backgroundImage,imageDescription)

def formatMonth(year,month,image,backgroundImage,imageDescription):
	# month frame with background
	bg = "background-image:url({});".format(backgroundImage)
	with div(cls="page month",style=bg):
		# image
		with div(cls="month-image-container"):
			with div(cls="month-image-aspect-ratio"):
				img(src=image,cls="month-image",alt="")
		# image description
		div(imageDescription,cls="month-image-description")
		# month name and year
		with div(cls="month-description"):
			div(month.name,cls="month-name")
			div(year,cls="month-year")
		formatDays(month,year)

def formatDays(month,year):
	with div(cls="days"):
		with div(cls="days-line days-line-1"):
			names = [d.abbrName for d in month.weeks[0].days]
			for name in names:
				div(name,cls="day-weekday-name")
		for week in month.weeks:
			if all(day.date.year != year for day in week.days if day.month is month):
				continue
			formatWeek(week,month,year)

def formatWeek(week,month,year):
	with div(cls="days-line"):
		for day in week.days:
			formatDay(day,month,year)

def formatDay(day,month,year):
	if not day.month is month or day.date.year != year:
		div(cls="day")
		return
	# collect classes
	wd = day.date.weekday()
	dayname = getWeekDayName(wd)
	classes = ["day","day-{}".format(dayname)]
	if day.publicHoliday:
		classes.append("day-is-public-holiday")
	if day.religiousHoliday:
		classes.append("day-is-religious-holiday")
	if day.note:
		classes.append("day-is-note")
	cls = " ".join(classes)
	# day div
	with div(cls=cls):
		# name
		number = "{}".format(day.date.day)
		div(number,cls="day-number")
		# name-day
		div(day.nameDay,cls="day-name-day")
		# religious holiday
		div(day.religiousHoliday,cls="day-religious-holiday")
		# public holiday
		p = "" if day.nameDay == day.publicHoliday else day.publicHoliday
		div(p,cls="day-public-holiday")
		# note
		div(day.note,cls="day-note")

# template mandatory toHTMLString(calendar) function
def toHTMLString(calendar):
	doc = createDoc(calendar)
	with doc.body:
		formatTitlePage(calendar)
		formatMonths(calendar)
	toString = str if six.PY3 else unicode
	return toString(doc)

# template mandatory CSSString constant
CSSString = loadCSS(__file__)
