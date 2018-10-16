import os, sys
from tempfile import gettempdir
from photocalendar import PhotoCalendar
sys.path.append(os.pardir)
from preprocessExample import main as preprocessExample

# locale and directory of corresponding data
locale = "cs_CZ"
dirLocale = os.path.join(os.pardir,os.pardir,"locale",locale)

# directories to be used. If you want to build your own calendar, you can use the same directory structure
buildDirectory            = os.path.join(gettempdir(),"photocalendar-example1")   # main build directory
dataDirectory             = os.path.join(buildDirectory,"data")                   # where auxiliary data will be put ...
imagesDirectory           = os.path.join(dataDirectory,"images")                  # ... e.g. images ...
imageDescriptionsFile     = os.path.join(dataDirectory,"imageDescriptions.dat")   # ... their decriptions ...
backgroundImagesDirectory = os.path.join(dataDirectory,"backgrounds")             # ... backgrounds
title                     = "PhotoCalendar 2019"                                  # ... title
titlePageImage            = os.path.join(dataDirectory,"titlePageImage.svg")      # ... title image
titlePageBackground       = os.path.join(dataDirectory,"titlePageBackground.svg") # ... title background
notesFile                 = os.path.join(dataDirectory,"notes.dat")               # ... or notes for days
nameDaysFile              = os.path.join(dataDirectory,"nameDays.dat")            # ... or name-days
religiousHolidaysFile     = os.path.join(dataDirectory,"religiousHolidays.dat")   # ... or religious holidays
publicHolidaysFile        = os.path.join(dataDirectory,"publicHolidays.dat")      # ... or public holidays
weekDayNamesFile          = os.path.join(dataDirectory,"weekDayNames.dat")        # ... or custom names of week days
monthNamesFile            = os.path.join(dataDirectory,"monthNames.dat")          # ... or custom names of months

# create sample images and other data
preprocessExample(buildDirectory,locale=locale)

# create the calendar and save it
calendar = PhotoCalendar(
	outputBase                = os.path.join(buildDirectory,"example1-py"),
	year                      = 2019,
	firstWeekDay              = "Tu",
	imagesDirectory           = imagesDirectory,
	imageDescriptionsFile     = imageDescriptionsFile,
	backgroundImagesDirectory = backgroundImagesDirectory,
	title                     = title,
	titlePageImage            = titlePageImage,
	titlePageBackground       = titlePageBackground,
	nameDaysFile              = nameDaysFile,
	religiousHolidaysFile     = religiousHolidaysFile,
	publicHolidaysFile        = publicHolidaysFile,
	notesFile                 = notesFile,
	weekDayNamesFile          = weekDayNamesFile,
	monthNamesFile            = monthNamesFile,
)
calendar.toHTML()
