import os
import unittest
from tempfile import gettempdir
from photocalendar import PhotoCalendar

tmp = os.path.join(gettempdir(),"photocalendar-tmp")

class TestCalendar(unittest.TestCase):
	def test_shouldPass(self):
		return
		args = dict(
			outputBase = os.path.join(gettempdir(),"photocalendar-test1"),
			year = 2019,
		)
		calendar = PhotoCalendar(**args)
		calendar.toHTML()
	def test_firstWeekDay(self):
		calendar = PhotoCalendar(tmp,firstWeekDay="mo")
		calendar = PhotoCalendar(tmp,firstWeekDay="SU")
		with self.assertRaisesRegexp(AssertionError,"invalid firstWeekDay 'nonsense'"):
			calendar = PhotoCalendar(tmp,firstWeekDay="nonsense")
