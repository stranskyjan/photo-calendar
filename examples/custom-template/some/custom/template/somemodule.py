# TODO

def head(calendar):
	return u"""
		<head>
			<meta charset="utf-8">
			<link rel="stylesheet" href="{css}">
		</head>
		""".format(css=calendar.outputBase+".css")

def body(calendar):
	ret = u"""
		<body>
			<div style="
				position: relative;
				width: 210mm;
				height: 297mm;
			">
				<img alt="" src="{titlePageImage}" style="
					position: absolute;
					width: 100%;
					height: 100%;
					page-break-after: always;
				">
				<span style="
					position: relative;
					font-size: 300%;
				">
					{title}
				</span>
			</div>
			{weeks}
		</body>
	""".format(
		titlePageImage = calendar.titlePageImage,
		title = calendar.title,
		weeks = weeks(calendar),
	)
	return ret

def weeks(calendar):
	return u"\n".join(week(calendar.weeks[i]) for i in range(53))

def week(week):
	return u"""
		<div style="
			position: relative;
			width: 210mm;
			height: 297mm;
			page-break-after: always;
		">
			<img alt="" src="{image}" style="
				position: absolute;
				width: 100%;
				height: 100%;
				z-index: -1000;
			">
			Week number {number}
			<div>{month1}-{month2}</div>
			{days}
		</div>
	""".format(
		image = week.imagePath,
		number = week.number,
		month1 = week.month1.name,
		month2 = week.month2.name,
		days = days(week.days)
	)

def days(days):
	return u"\n".join(day(d) for d in days)

def day(day):
	return u"""
		<div>
			{name} {number} {nameDay} {publicHoliday}
		</div>
	""".format(
		name = day.name,
		number = day.date.day,
		nameDay = day.nameDay,
		publicHoliday = day.publicHoliday,
	)

def toHTMLString(calendar):
	ret = u"""
		<!DOCTYPE html>
		<html>
			{head}
			{body}
		</html>
		""".format(head=head(calendar),body=body(calendar))
	return u"\n".join(filter(None, map(lambda l: l.strip(), ret.split("\n"))))

