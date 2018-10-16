# See ../example1 for more info
import os, sys
from tempfile import gettempdir
from photocalendar import PhotoCalendar
sys.path.append(os.pardir)
from preprocessExample import main as preprocessExample

locale = "cs_CZ"
dirLocale = os.path.join(os.pardir,os.pardir,"locale",locale)

buildDirectory            = os.path.join(gettempdir(),"photocalendar-custom-template")
dataDirectory             = os.path.join(buildDirectory,"data")
imagesDirectory           = os.path.join(dataDirectory,"images")
imageDescriptionsFile     = os.path.join(dataDirectory,"imageDescriptions.dat")
title                     = "Custom Teamplate 2019"
titlePageImage            = os.path.join(dataDirectory,"titlePageImage.svg")
notesFile                 = os.path.join(dataDirectory,"notes.dat")
nameDaysFile              = os.path.join(dataDirectory,"nameDays.dat")
publicHolidaysFile        = os.path.join(dataDirectory,"publicHolidays.dat")
template                  = os.path.join(os.pardir,"custom-template","some","custom","template")

preprocessExample(buildDirectory,locale=locale)

calendar = PhotoCalendar(
	outputBase                = os.path.join(buildDirectory,"custom-template-py"),
	year                      = 2019,
	imagesDirectory           = imagesDirectory,
	title                     = title,
	titlePageImage            = titlePageImage,
	nameDaysFile              = nameDaysFile,
	publicHolidaysFile        = publicHolidaysFile,
	notesFile                 = notesFile,
	template                  = template,
)
calendar.toHTML()
