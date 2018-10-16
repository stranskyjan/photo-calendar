import os
import datetime
import codecs
import six
from six import string_types
from .templates import loadTemplate

_NWEEKS = 53

######################################################################
class Day:
	"""
	Class representing a day.
	It contains all necessary info for the calendar.
	
	:param datetime.date date: datetime.date instance for the day
	:param str name: name of the day (e.g. Monday)
	:param str nameDay: name day, saint's day (e.g. Jan, Patrik, ...)
	:param str religiousHoliday: name of religious holidays (e.g. Easter, Chinese New Year, Ramadan, Pesach, ...)
	:param str publicHoliday: name of public holiday (e.g. Labour day, Independence day, German Unity Day, ...)
	:param str note: note (e.g. a friend's birthday, wedding anniversary, ...)
	"""
	def __init__(self, date, name = u"", nameDay = u"", religiousHoliday = u"", publicHoliday = u"", note = u""):
		self.date = date
		self.name = name
		self.nameDay = nameDay
		self.religiousHoliday = religiousHoliday
		self.publicHoliday = publicHoliday
		self.note = note

class Week:
	"""
	Class representing a week.
	It contains 7 :class:`days <photocalendar.Day>`, beginning and ending :class:`months <photocalendar.Month>` and info about images
	
	:param days: tuple of 7 :class:`Day <photocalendar.Day>` instances
	:type days: tuple(:class:`Day <photocalendar.Day>`)
	:param month1: :class:`Month <photocalendar.Month>` instance of the first day of the week
	:type month1: :class:`Month <photocalendar.Month>`
	:param month2: :class:`Month <photocalendar.Month>` instance of the last day of the week
	:type month2: :class:`Month <photocalendar.Month>`
	:param str imagePath: path to image for the week
	:param str imageDescription: image description
	:param str backgroundImagePath: path to background image
	"""
	def __init__(self, days, number=-1, month1=None, month2=None, imagePath="", imageDescription="", backgroundImagePath=""):
		self.days = tuple(days)
		assert len(days) == 7
		self.number = number
		self.month1 = month1
		self.month2 = month2
		self.imagePath = imagePath
		self.imageDescription = imageDescription
		self.backgroundImagePath = backgroundImagePath

class Month:
	"""
	Class representing a month
	
	:param str name: name of the month
	"""
	def __init__(self, name=u""):
		self.name = name
######################################################################



def _loadLinesFromFile(fName):
	with codecs.open(fName,encoding="utf-8") as f:
		ret = f.readlines()
	ret = [l.strip().partition("#")[0] for l in ret]
	ret = [l for l in ret if l]
	return ret

def _lines2monthDict(lines):
	ret = dict((i+1,{}) for i in range(12))
	for line in lines:
		ls = line.split()
		m,d = [int(ls[i]) for i in (0,1)]
		data = " ".join(ls[2:])
		ret[m][d] = data
	return ret

_attrdocs = dict(
	outputBase                = "file base for outputs",
	year                      = "calendar year (default is the next year from today)",
	firstWeekDay              = "first weekday (passed as first two letters of English name). Default is MO",
	imagesDirectory           = "path to directory with week images. There have to be exactly 53 files, they are used in alphabetical order",
	imageDescriptionsFile     = "file with exactly 53 descriptions used to annotate week images",
	backgroundImagesDirectory = "path to directory with background images. There have to be exactly 53 files, they are used in alphabetical order",
	title                     = "calendar title",
	titlePageImage            = "path to title page image",
	titlePageBackground       = "path to title page background image",
	nameDaysFile              = "file with name-days, see ``locale/cs_CZ/dayNames.dat`` for illustration",
	religiousHolidaysFile     = "file with religious holidays, see ``examples/religiousHolidays.dat`` for illustration",
	publicHolidaysFile        = "file with public holidays, see ``locale/cs_CZ/publicHolidays.dat`` for illustration",
	notesFile                 = "file with notes, see ``examples/notes.dat`` for illustration",
	weekDayNamesFile          = "file with custom weekday names. If not specifed, names from locale are used.",
	monthNamesFile            = "file with custom month names. If not specifed, names from locale are used.",
	template                  = """template name to be used for HTML/CSS formatting. It is:
		
		1) name of package predefined template (e.g. ``delphinus``)
		2) TODO custom templates
		""",
)

class PhotoCalendar:
	"""
	Main class containing 

	:param str outputBase: {outputBase}
	:param int year: {year}
	:param str firstWeekDay: {firstWeekDay}
	:param str imagesDirectory: {imagesDirectory}
	:param str imageDescriptionsFile: {imageDescriptionsFile}
	:param str backgroundImagesDirectory: {backgroundImagesDirectory}
	:param str title: {title}
	:param str titlePageImage: {titlePageImage}
	:param str titlePageBackground: {titlePageBackground}
	:param str nameDaysFile: {nameDaysFile}
	:param str religiousHolidaysFile: {religiousHolidaysFile}
	:param str publicHolidaysFile: {publicHolidaysFile}
	:param str notesFile: {notesFile}
	:param str weekDayNamesFile: {weekDayNamesFile}
	:param str monthNamesFile: {monthNamesFile}
	:param str template: {template}
	"""
	def __init__(self,
			outputBase                = u"",
			year                      = datetime.date.today().year + 1,
			firstWeekDay              = u"MO",
			imagesDirectory           = u"",
			imageDescriptionsFile     = u"",
			backgroundImagesDirectory = u"",
			title                     = u"",
			titlePageImage            = u"",
			titlePageBackground       = u"",
			nameDaysFile              = u"",
			religiousHolidaysFile     = u"",
			publicHolidaysFile        = u"",
			notesFile                 = u"",
			weekDayNamesFile          = u"",
			monthNamesFile            = u"",
			template                  = "delphinus",
	):
		self.outputBase = outputBase
		self.year = int(year)
		self.firstWeekDay = firstWeekDay
		self.imagesDirectory = imagesDirectory
		self.imageDescriptionsFile = imageDescriptionsFile
		self.backgroundImagesDirectory = backgroundImagesDirectory
		self.title = title
		self.titlePageImage = titlePageImage
		self.titlePageBackground = titlePageBackground
		self.nameDaysFile = nameDaysFile
		self.religiousHolidaysFile = religiousHolidaysFile
		self.publicHolidaysFile = publicHolidaysFile
		self.notesFile = notesFile
		self.template = template
		self.weekDayNamesFile = weekDayNamesFile
		self.monthNamesFile = monthNamesFile
		#
		self._firstWeekDayId = None
		#: names of weekdays
		self.weekDayNames = None
		#: names of months
		self.monthNames = None
		#: list of 53 or 0 image urls to be used for weeks
		self.images = None
		#: list of 53 or 0 image urls to be used as background for weeks
		self.backgroundImages = None
		#: list of 53 or 0 description of week images
		self.imageDescriptions = None
		#: dict(dict) of name-days, e.g. self.nameDays[6][24], 24th June, would be Jan (John) in Czech
		self.nameDays = None
		#: dict(dict) of religious holidays, e.g. self.religiousHolidays[11][1], 1st November, could be All Saints' Day
		self.religiousHolidays = None
		#: dict(dict) of public holidays, e.g. self.publicHolidays[7][4], 4th July, would be Independence Day in US
		self.publicHolidays = None
		#: dict(dict) of notes, e.g. self.notes[5][4] could be Star Wars Day
		self.notes = None
		#
		#: Function to create HTML string of the calendar (loaded from template)
		self.toHTMLString = None
		#: CSS file to be used with produced HTML (loaded from template)
		self.CSSString = None
		#
		self.check()
		self.loadMetadata()
		self.build()
	def check(self):
		"""checks if all arguments (e.g. firstWeekDay, template) has correct values"""
		fwd = self.firstWeekDay.upper()
		days = ("MO","TU","WE","TH","FR","SA","SU")
		assert fwd in days, "invalid firstWeekDay '{}'".format(self.firstWeekDay)
		self._firstWeekDayId = days.index(fwd)
		#
		template = loadTemplate(self.template)
		assert template, "Unable to load template '{}'".format(self.template)
		self.toHTMLString, self.CSSString = template
		assert callable(self.toHTMLString), "template toHTMLString has to be function"
		# TODO assert 1 parameter ?
		assert isinstance(self.CSSString,string_types), "template CSSString has to be string"
	def build(self):
		"""builds the calendar (create days, weeks, load everything needed, ...)"""
		d = datetime.date(self.year,1,1)
		while d.weekday() != self._firstWeekDayId:
			d -= datetime.timedelta(days=1)
		self.weeks = []
		while True:
			days = [Day(d + datetime.timedelta(days=i)) for i in range(7)]
			d += datetime.timedelta(days=7)
			self.weeks.append(Week(days))
			if d.year != self.year:
				break
		#
		self.months = dict((i+1,Month(name)) for i,name in enumerate(self.monthNames))
		#
		for iweek,week in enumerate(self.weeks):
			week.number = iweek+1
			m1,m2 = [self.months[week.days[i].date.month] for i in (0,-1)]
			week.month1 = m1
			week.month2 = m2
			if self.images:
				week.imagePath = self.images[iweek]
			if self.backgroundImages:
				week.backgroundImagePath = self.backgroundImages[iweek]
			if self.imageDescriptions:
				week.imageDescription = self.imageDescriptions[iweek]
			for day in week.days:
				m = day.date.month
				d = day.date.day
				w = day.date.weekday()
				day.name = self.weekDayNames[w]
				if self.nameDays:
					day.nameDay = self.nameDays[m].get(d,u"")
				if self.religiousHolidays:
					day.religiousHoliday = self.religiousHolidays[m].get(d,u"")
				if self.publicHolidays:
					day.publicHoliday = self.publicHolidays[m].get(d,u"")
				if self.notes:
					day.note = self.notes[m].get(d,u"")
	def loadMetadata(self):
		"""load everything needed (e.g. month names, images, holidays, ...)"""
		self.loadLocaleNames()
		self.loadImages()
		self.loadBackgroundImages()
		self.loadImageDescriptions()
		self.loadNameDays()
		self.loadReligiousHolidays()
		self.loadPublicHolidays()
		self.loadNotes()
	def loadLocaleNames(self):
		"""Loads weekday and month names from files. If files are not specified, set the names according to locale package"""
		if self.weekDayNamesFile:
			self.weekDayNames = _loadLinesFromFile(self.weekDayNamesFile)
			assert len(self.weekDayNames) == 7
		else:
			import locale
			self.weekDayNames = [locale.nl_langinfo(getattr(locale,"DAY_{}".format(1+(i+2)%7))) for i in range(7)]
			if six.PY2:
				self.weekDayNames = [n.decode("utf-8") for n in self.weekDayNames]
		#
		if self.monthNamesFile:
			self.monthNames = _loadLinesFromFile(self.monthNamesFile)
			assert len(self.monthNames) == 12
		else:
			import locale
			self.monthNames = [locale.nl_langinfo(getattr(locale,"MON_{}".format(i+1))) for i in range(12)]
			if six.PY2:
				self.monthNames = [n.decode("utf-8") for n in self.monthNames]
	def loadImages(self):
		"""load images according to given directory. The directory has to contain exactly 53 files. They are used in alphabetical order"""
		self.images = None
		if not self.imagesDirectory:
			return
		fs = os.listdir(self.imagesDirectory)
		self.images = sorted(os.path.abspath(os.path.join(self.imagesDirectory,f)) for f in fs)
		assert len(self.images) == _NWEEKS
	def loadBackgroundImages(self):
		"""load background images according to given directory. The directory has to contain exactly 53 files. They are used in alphabetical order"""
		self.backgroundImages = None
		if not self.backgroundImagesDirectory:
			return
		fs = os.listdir(self.backgroundImagesDirectory)
		self.backgroundImages = sorted(os.path.abspath(os.path.join(self.backgroundImagesDirectory,f)) for f in fs)
		assert len(self.backgroundImages) == _NWEEKS
	def loadImageDescriptions(self):
		"""
		load image descriptions from given file. empty lines are skipped.
		# symbol is considered as comment.
		The format of valid line is 'month day note'.
		E.g. to have note 'Star Wars Day' on May the fourth, the corresponding line would be '5 4 Star Wars Day'.
		Any number of spaces/tabs can be used as delimiters.
		"""
		self.imageDescriptions = None
		if not self.imageDescriptionsFile:
			return
		self.imageDescriptions = _loadLinesFromFile(self.imageDescriptionsFile)
		assert len(self.imageDescriptions) == _NWEEKS
	def loadNameDays(self):
		"""load name-days from given file (if provided)"""
		self.nameDays = None
		if not self.nameDaysFile:
			return
		self.nameDays = _lines2monthDict(_loadLinesFromFile(self.nameDaysFile))
	def loadReligiousHolidays(self):
		"""load religious holidays from given file (if provided)"""
		self.religiousHolidays = None
		if not self.religiousHolidaysFile:
			return
		self.religiousHolidays = _lines2monthDict(_loadLinesFromFile(self.religiousHolidaysFile))
	def loadPublicHolidays(self):
		"""load public holidays from given file (if provided)"""
		self.publicHolidays = None
		if not self.publicHolidaysFile:
			return
		self.publicHolidays = _lines2monthDict(_loadLinesFromFile(self.publicHolidaysFile))
	def loadNotes(self):
		"""load notes from given file (if provided)"""
		self.notes = None
		if not self.notesFile:
			return
		self.notes = _lines2monthDict(_loadLinesFromFile(self.notesFile))
	def toHTML(self):
		"""Saves the calendar in html file (uses toHTMLString function loaded from template)"""
		htmlString = self.toHTMLString(self)
		with codecs.open("{}.html".format(self.outputBase),"w",encoding="utf-8") as f:
			f.write(htmlString)
		with codecs.open("{}.css".format(self.outputBase),"w",encoding="utf-8") as f:
			f.write(self.CSSString)

PhotoCalendar.__doc__ = PhotoCalendar.__doc__.format(**_attrdocs)
