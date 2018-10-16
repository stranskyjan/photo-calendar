#!/bin/sh
# This file is a "shell copy" of corresponding python example, see it for ore info
# This file assumes the python version to be run first (creates directories, figs etc.)

dirBuild=/tmp/photocalendar-example1
dirData=$dirBuild/data
imagesDirectory=$dirData/images
imageDescriptionsFile=$dirData/imageDescriptions.dat
backgroundImagesDirectory=$dirData/backgrounds
title="PhotoCalendar 2019"
titlePageImage=$dirData/titlePageImage.png
titlePageBackground=$dirData/titlePageBackground.png
notesFile=$dirData/notes.dat
nameDaysFile=$dirData/nameDays.dat
religiousHolidaysFile=$dirData/religiousHolidays.dat
publicHolidaysFile=$dirData/publicHolidays.dat
weekDayNamesFile=$dirData/weekDayNames.dat
monthNamesFile=$dirData/monthNames.dat

photocalendar \
	--output-base                 $dirBuild/example1-sh \
	--year                        2019 \
	--first-weekday               Tu \
	--images-directory            $imagesDirectory \
	--image-descriptions-file     $imageDescriptionsFile \
	--background-images-directory $backgroundImagesDirectory \
	--title                       "$title" \
	--title-page-image            $titlePageImage \
	--title-page-background       $titlePageBackground \
	--name-days-file              $nameDaysFile \
	--religious-holidays-file     $religiousHolidaysFile \
	--public-holidays-file        $publicHolidaysFile \
	--notes-file                  $notesFile \
	--week-day-names-file         $weekDayNamesFile \
	--month-names-file            $monthNamesFile
