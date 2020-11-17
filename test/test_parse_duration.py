import logging
import unittest

from datetime import timedelta

import wxdat

# keep logging output to a minumim for testing
logging.basicConfig(level=logging.FATAL)

################################################################################
class ParseDuration(unittest.TestCase):

    #---------------------------------------------------------------------------
    def test_BasicLongForm(self):
        delta = wxdat.parse_duration('01:32:07')
        expect = timedelta(hours=1, minutes=32, seconds=7)
        self.assertEqual(delta, expect)

    #---------------------------------------------------------------------------
    def test_ModifiedLongForm(self):
        delta = wxdat.parse_duration('28:47')
        expect = timedelta(minutes=28, seconds=47)
        self.assertEqual(delta, expect)

    #---------------------------------------------------------------------------
    def test_ShortFormHours(self):
        delta = wxdat.parse_duration('2h')
        expect = timedelta(hours=2)
        self.assertEqual(delta, expect)

    #---------------------------------------------------------------------------
    def test_ShortFormMinutes(self):
        delta = wxdat.parse_duration('30m')
        expect = timedelta(minutes=30)
        self.assertEqual(delta, expect)

    #---------------------------------------------------------------------------
    def test_ShortFormSeconds(self):
        delta = wxdat.parse_duration('23s')
        expect = timedelta(seconds=23)
        self.assertEqual(delta, expect)

    #---------------------------------------------------------------------------
    def test_FullShortForm(self):
        delta = wxdat.parse_duration('2h 14m 23s')
        expect = timedelta(hours=2, minutes=14, seconds=23)
        self.assertEqual(delta, expect)

