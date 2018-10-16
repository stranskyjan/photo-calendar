#!/bin/sh
# This file is a "shell copy" of corresponding python example, see it for ore info
# This file assumes the python version to be run first (creates directories, figs etc.)

dirBuild=/tmp/photocalendar-custom-template
dirData=$dirBuild/data
imagesDirectory=$dirData/images
title="Custom Teamplate 2019"
titlePageImage=$dirData/titlePageImage.svg
notesFile=$dirData/notes.dat
nameDaysFile=$dirData/nameDays.dat
publicHolidaysFile=$dirData/publicHolidays.dat
template=../custom-template/some/custom/template

photocalendar \
	--output-base                 $dirBuild/custom-template-sh \
	--year                        2019 \
	--images-directory            $imagesDirectory \
	--title                       "$title" \
	--title-page-image            $titlePageImage \
	--name-days-file              $nameDaysFile \
	--public-holidays-file        $publicHolidaysFile \
	--notes-file                  $notesFile \
	--template                    $template
