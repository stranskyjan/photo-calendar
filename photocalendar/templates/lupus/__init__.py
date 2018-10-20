"""
A very basic tamplate for two-week calendar.
Serving mainly as a reference for more sophisticated templates.
The paper size is half of A4 landscape (297x105).

**Title page**:

- centered
- title image aspect ratio is 2:1

**Weeks**:

- image in the middle
- days on the left and on the right side
- days as lines separated by horizontal line on the right side
- image aspect ratio is 4:3
- image descriptions are below images
- week number and month name(s) are at the bottom of the page
"""
import os
import six
from .. import loadCSS
if 0: # you can use dominate if you like (the syntax is identical) ...
	from dominate import document
	from dominate.tags import meta,link,div,img,hr
else: # ... but the internal module is used by default
	from ..html import HTMLDocument as document
	from ..html import meta,link,div,img,hr


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

def formatDoubleWeeks(calendar):
	empty = ["" for _ in range(27)]
	images            = calendar.images            if calendar.images            else empty
	backgroundImages  = calendar.backgroundImages  if calendar.backgroundImages  else empty
	imageDescriptions = calendar.imageDescriptions if calendar.imageDescriptions else empty
	assert all(len(vs) >= 27 for vs in (images,backgroundImages,imageDescriptions))
	weeks1 = [week for week in calendar.weeks if week.number % 2 != 0]
	weeks2 = [week for week in calendar.weeks if week.number % 2 == 0] + [None]
	assert all(len(weeks) == 27 for weeks in (weeks1,weeks2))
	for week1,week2,image,backgroundImage,imageDescription in zip(weeks1,weeks2,images,backgroundImages,imageDescriptions):
		formatDoubleWeek(week1,week2,image,backgroundImage,imageDescription)

def formatDoubleWeek(week1,week2,image,backgroundImage,imageDescription):
	# week frame with background
	bg = "background-image:url({});".format(backgroundImage)
	with div(cls="page",style=bg):
		# image
		with div(cls="week-image-container"):
			with div(cls="week-image-aspect-ratio"):
				img(src=image,cls="week-image",alt="")
		# image description
		div(imageDescription,cls="week-image-description")
		# month name(s)
		month1 = week1.month1
		month2 = week2.month2 if week2 else month1
		if month1 is month2:
			monthName = month1.name
		else:
			monthName = u"{} / {}".format(month1.name,month2.name)
		div(monthName,cls="month-name")
		# days
		with div(cls="double-week"):
			with div(cls="week week-1"):
				formatWeek(week1)
			if week2:
				with div(cls="week week-2"):
					formatWeek(week2)

def formatWeek(week):
	hr()
	for day in week.days:
		formatDay(day)
		hr()
	# week number
	number = u"Week {}".format(week.number)
	div(number,cls="week-number")

def getWeekDayName(index):
	return ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")[index]

def formatDay(day):
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
		div(day.name,cls="day-name")
		# number
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

def formatLastPage(calendar):
	# last page with background and year calendar
	bg = "background-image:url({});".format(calendar.lastPageBackground)
	with div(cls="page",id="last-page",style=bg):
		# year
		div(calendar.year,id="last-page-year")
		# 2 lines of Jan-Jun and Jul-Dec months
		for months in (calendar.months[:6],calendar.months[6:]):
			with div(cls="last-page-months"):
				formatLastPageMonths(months,calendar.year)

def formatLastPageMonths(months,year):
	for month in months:
		formatLastPageMonth(month,year)

def formatLastPageMonth(month,year):
	# one full month
	with div(cls="last-page-month"):
		# month name
		div(month.name,cls="last-page-month-name")
		# weekday names abbreviations
		with div(cls="last-page-month-line last-page-month-line-1"):
			for day in month.weeks[0].days:
				name = day.abbrName
				wd = day.date.weekday()
				dayname = getWeekDayName(wd)
				classes = ["last-page-month-element","last-page-month-element-{}".format(dayname)]
				div(name,cls=u" ".join(classes))
		# weeks as line
		for week in month.weeks:
			with div(cls="last-page-month-line"):
				for day in week.days:
					number = day.date.day if day.month is month and day.date.year == year else ""
					if not number:
						div(cls="last-page-month-element")
						continue
					# collect classes
					wd = day.date.weekday()
					dayname = getWeekDayName(wd)
					classes = ["last-page-month-element","last-page-month-element-{}".format(dayname)]
					if day.publicHoliday:
						classes.append("last-page-month-element-is-public-holiday")
					if day.religiousHoliday:
						classes.append("last-page-month-element-is-religious-holiday")
					if day.note:
						classes.append("last-page-month-element-is-note")
					cls = " ".join(classes)
					div(number,cls=cls)

# template mandatory toHTMLString(calendar) function
def toHTMLString(calendar):
	doc = createDoc(calendar)
	with doc.body:
		formatTitlePage(calendar)
		formatDoubleWeeks(calendar)
		formatLastPage(calendar)
	toString = str if six.PY3 else unicode
	return toString(doc)

# template mandatory CSSString constant
CSSString = loadCSS(__file__)
