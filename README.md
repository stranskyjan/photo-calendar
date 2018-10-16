# PhotoCalendar
PhotoCalendar is a [Python](https://python.org) utility to create custom weekly photo calendars.
It creates the calendar in HTML format (which you can then print to PDF using browser or, e.g., [weasyptint utility](https://weasyprint.org)).
The user may provide (see examples below):
- name of weekdays and months
- images (for each week, for title page, for backgrounds)
- name-days
- public holidays
- religious holidays
- notes (friends' birthdays, anniversaries, ...)
- ...

The produced HTML structure as well as the CSS styling is fully customizable and (according to the author's opinion :-) flexible and easy to use.
See [examples](examples) and/or documentation for more information.
As an example and inspiration, one predefined theme `delphinus` is provided.

The package works with both Python 2 and 3 (tested on [Ubuntu 16.04 LTS](https://www.ubuntu.com/) and Python 2.7.12 and Python 3.5.2).

## Examples
Note:
the photos and backgrounds are only illustrative.
They are provided by the user in the real use case.

The title page (left) and the 18th week (right) is shown.

In the illustrations,
[picture](https://upload.wikimedia.org/wikipedia/commons/d/d1/Golden_Gate_1.jpg)
of
[Golden Gate Bridge](https://en.wikipedia.org/wiki/Golden_Gate_Bridge)
and
[picture](https://upload.wikimedia.org/wikipedia/commons/4/4c/Matterhorn_from_Zermatt2.jpg)
of
[Matterhorn](https://en.wikipedia.org/wiki/Matterhorn)
are used.

### Template delphinus:
![template delphinus](images/delphinus.png)

### Code example
##### using python:
```python
from photocalendar import PhotoCalendar
calendar = PhotoCalendar( # not all arguments are mandatory
	outputBase                = "/some/output/base",
	year                      = 2019,
	firstWeekDay              = "Tu", # Tuesday as the first week day? Well, why not...
	imagesDirectory           = "/some/directory/with/images/for/each/week",
	imageDescriptionsFile     = "/some/file/with/image/descriptions/for/each/week",
	backgroundImagesDirectory = "/some/directory/with/backround/images/for/each/week",
	title                     = "Some calendar title",
	titlePageImage            = "/some/image/for/title/page",
	titlePageBackground       = "/some/background/image/for/titlepage",
	nameDaysFile              = "/some/file/with/name-days",
	religiousHolidaysFile     = "/some/file/with/religious/holidays",
	publicHolidaysFile        = "/some/file/with/public/holidays",
	notesFile                 = "/some/file/with/notes/like/birthdays/etc",
	weekDayNamesFile          = "/some/file/with/custom/week/day/names",
	monthNamesFile            = "/some/file/with/custom/month/names",
)
calendar.toHTML()
```

##### using shell:
```shell
# not all arguments are mandatory
photocalendar \
	--output-base                 /some/output/base \
	--year                        2019 \
	--first-week-day              Tu \ # Tuesday as the first week day? Well, why not...
	--images-directory            /some/directory/with/images/for/each/week  \
	--image-descriptions-file     /some/file/with/image/descriptions/for/each/week \
	--background-images-directory /some/directory/with/backround/images/for/each/week \
	--title                       "Some calendar title" \
	--title-page-image            /some/image/for/title/page \
	--title-page-background       /some/background/image/for/titlepage \
	--name-days-file              /some/file/with/name-days \
	--religious-holidays-file     /some/file/with/religious/holidays \
	--public-holidays-file        /some/file/with/public/holidays \
	--notes-file                  /some/file/with/notes/like/birthdays/etc \
	--week-day-names-file         /some/file/with/custom/week/day/names \
	--month-names-file            /some/file/with/custom/month/names
```

## What is here
| file/directory | description |
| --- | --- |
| [bin](bin) | directory containing executable python script |
| [doc](doc) | source files for HTML documentation |
| [examples](examples) | directory with examples |
| [images](images) | images for github page (e.g., templates illustrations) |
| [locale](locale) | files for localization (public holidays, name days, etc.) |
| [Makefile](Makefile) | makefile for the project (with targets `help`, `install`, `doc`, `test`, `clean`) |
| [photocalendar](photocalendar) | actual python package |
| [setup.py](setup.py) | python setup file for installation |
| [tests](tests) | python unit tests |

## Acknowledgement
- to Petr Hlaváček for the inital idea and LaTeX implementation and providing his source code
- to [dominate python package](https://github.com/Knio/dominate) for HTML creation inspiration

## TODO
- more templates
- support for custom templates
- monthly calendar?
