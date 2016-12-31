import sys # noqa
sys.path.append('../wikidict') # noqa

from wikidict.wikidict import get_summary
import unittest2


class WikiddictTestCase(unittest2.TestCase):

    """Tests for `wikidict/wikidict.py`."""

    def test_get_summary_google_found(self):
        self.assertNotEqual(None, get_summary("Google", "en"))

    def test_get_summary_not_found(self):
        self.assertEqual(None, get_summary("Something that does not exist on wikipedia and that will never exist", "en"))


if __name__ == "__main__":
    unittest2.main()
