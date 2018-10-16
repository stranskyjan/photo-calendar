import unittest
from photocalendar.templates import html

class TestHtml(unittest.TestCase):
	def test_1(self):
		doc = html.HTMLDocument(title="abcd")
		with doc.head:
			html.script("var a=1;")
			html.meta(charset="utf-8")
		with doc.body:
			html.h1("title1")
			html.br()
			with html.div(cls="container"):
				html.span("text text",id="span-1")
				html.div()
		a = u"".join(list(map(lambda l: l.strip(), str(doc).split("\n"))))
		e = u"".join((
			'<!DOCTYPE html>',
			'<html>',
				'<head>',
					'<title>abcd</title>',
					'<script>var a=1;</script>',
					'<meta charset="utf-8">',
				'</head>',
				'<body>',
					'<h1>title1</h1>',
					'<br>',
					'<div class="container">',
						'<span id="span-1">text text</span>',
						'<div></div>',
					'</div>',
				'</body>',
			'</html>',
		))
		self.assertEqual(e,a)
