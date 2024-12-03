import sys
sys.path.append('../wikiluv')

from wikiluv import *
import unittest2
import requests
import sys

class WikiddictTestCase(unittest2.TestCase):

    """Tests for `wikiluv/wikiluv.py`."""

    def setUp(self):
        self.query = "google"
        self.lang = "en"
        self.summary_default = "Not Found"
    
    def test_get_summary(self):
        get_summary(self.query, self.lang)
        self.assertNotEqual(Info.SUMMARY, self.summary_default, msg = "No data found for the given query")
           
if __name__ == "__main__":
    unittest2.main()