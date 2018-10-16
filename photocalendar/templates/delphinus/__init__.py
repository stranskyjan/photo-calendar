"""
A very basic tamplate serving mainly as a reference for more sophisticated templates.

**Title page**:

- centered
- title image aspect ratio is 16:9.

**Weeks**:

- image on the left side
- days on the right side
- days as lines separated by horizontal line on the right side
- images are square
- image descriptions are below images
- week number and month name(s) are at the top, above days
"""
import os
import six
from .. import loadCSS
if 0: # you can use dominate if you like (the syntax is identical) ...
	from dominate import document
	from dominate.tags import meta,link,div,img
else: # ... but the internal module is used by default
	from ..html import HTMLDocument as document
	from ..html import meta,link,div,img,hr

class HTMLFormatter:
	"""Auxiliary class to create a HTML file from given PhotoCalendar instance. See also corresponding CSS form some more info."""
	def createDoc(self,calendar):
		self.doc = document(title=calendar.title) # use calendar.title
		with self.doc.head:
			meta(charset="utf-8")
			link(rel='stylesheet', href="{}.css".format(os.path.basename(calendar.outputBase))) # add CSS file
	def formatTitlePage(self,calendar):
		# title page frame with background
		bg = "background-image:url({});".format(calendar.titlePageBackground)
		with div(cls="page",id="title-page",style=bg):
			# title image
			with div(id="title-page-image-container"):
				with div(id="title-page-image-aspect-ratio"):
					img(src=calendar.titlePageImage,alt="",id="title-page-image")
			# title
			div(calendar.title,id="title")
	def formatWeeks(self,calendar):
		for week in calendar.weeks:
			self.formatWeek(week)
	def formatWeek(self,week):
		# week frame with background
		mids = set(week.days[i].date.month for i in (0,-1))
		bg = "background-image:url({});".format(week.backgroundImagePath)
		with div(id="week-{}".format(week.number),cls="page week",style=bg):
			# image
			with div(cls="week-image-container"):
				with div(cls="week-image-aspect-ratio"):
					img(src=week.imagePath,cls="week-image",alt="")
			# image description
			div(week.imageDescription,cls="week-image-description")
			# month name(s)
			m1,m2 = week.month1,week.month2
			if m1 is m2:
				monthName = m1.name
			else:
				monthName = u"{} / {}".format(m1.name,m2.name)
			div(monthName,cls="month-name")
			# week number
			number = u"Week {}".format(week.number)
			div(number,cls="week-number")
			# days
			self.formatDays(week.days)
	def formatDays(self,days):
		with div(cls="days"):
			hr()
			for day in days:
				self.formatDay(day)
				hr()
	def formatDay(self,day):
		# collect classes
		wd = day.date.weekday()
		dayname = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")[wd]
		classes = ["day","day-{}".format(dayname)]
		if day.publicHoliday:
			classes.append("day-is-public-holiday")
		if day.religiousHoliday:
			classes.append("day-is-religious-holiday")
		if day.note:
			classes.append("day-isnote")
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
	def toHTMLString(self,calendar):
		self.createDoc(calendar)
		with self.doc.body:
			self.formatTitlePage(calendar)
			self.formatWeeks(calendar)
		toString = str if six.PY3 else unicode
		return toString(self.doc)

# template mandatory members
CSSString = loadCSS(__file__)
toHTMLString = lambda calendar: HTMLFormatter().toHTMLString(calendar)
