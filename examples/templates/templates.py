# see ../example1 for more info
import os, sys
from tempfile import gettempdir
from photocalendar import PhotoCalendar
sys.path.append(os.pardir)
from preprocessExample import main as preprocessExample

locale = "cs_CZ"
dirLocale = os.path.join(os.pardir,os.pardir,"locale",locale)

templates = (
	"delphinus",
	"columba",
	"lupus",
)
for template in templates:
	buildDirectory            = os.path.join(gettempdir(),"photocalendar-templates-{}".format(template))
	dataDirectory             = os.path.join(buildDirectory,"data")
	imagesDirectory           = os.path.join(dataDirectory,"images")
	imageDescriptionsFile     = os.path.join(dataDirectory,"imageDescriptions.dat")
	backgroundImagesDirectory = os.path.join(dataDirectory,"backgrounds")
	title                     = "PhotoCalendar 2019"
	titlePageImage            = os.path.join(dataDirectory,"titlePageImage.svg")
	titlePageBackground       = os.path.join(dataDirectory,"titlePageBackground.svg")
	lastPageBackground        = os.path.join(dataDirectory,"lastPageBackground.svg")
	notesFile                 = os.path.join(dataDirectory,"notes.dat")
	nameDaysFile              = os.path.join(dataDirectory,"nameDays.dat")
	religiousHolidaysFile     = os.path.join(dataDirectory,"religiousHolidays.dat")
	publicHolidaysFile        = os.path.join(dataDirectory,"publicHolidays.dat")
	weekDayNamesFile          = os.path.join(dataDirectory,"weekDayNames.dat")
	abbrWeekDayNamesFile      = os.path.join(dataDirectory,"abbrWeekDayNames.dat")
	monthNamesFile            = os.path.join(dataDirectory,"monthNames.dat")
	abbrMonthNamesFile        = os.path.join(dataDirectory,"abbrMonthNames.dat")

	preprocessExample(buildDirectory,locale=locale)

	calendar = PhotoCalendar(
		outputBase                = os.path.join(buildDirectory,"{}-py".format(template)),
		year                      = 2019,
		firstWeekDay              = "Tu",
		imagesDirectory           = imagesDirectory,
		imageDescriptionsFile     = imageDescriptionsFile,
		backgroundImagesDirectory = backgroundImagesDirectory,
		title                     = title,
		titlePageImage            = titlePageImage,
		titlePageBackground       = titlePageBackground,
		lastPageBackground        = lastPageBackground,
		nameDaysFile              = nameDaysFile,
		religiousHolidaysFile     = religiousHolidaysFile,
		publicHolidaysFile        = publicHolidaysFile,
		notesFile                 = notesFile,
		weekDayNamesFile          = weekDayNamesFile,
		abbrWeekDayNamesFile      = abbrWeekDayNamesFile,
		monthNamesFile            = monthNamesFile,
		abbrMonthNamesFile        = abbrMonthNamesFile,
		template                  = template
	)
	calendar.toHTML()
