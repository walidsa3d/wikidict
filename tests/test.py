import sys # noqa
sys.path.append('../wikidict') # noqa

from wikidict.wikidict import WikipediaClient
import unittest2


# helper function
def get_summary(query, lang):
    wd = WikipediaClient(query, lang)
    wd.make_query()
    return wd.get_summary()


class WikiddictTestCase(unittest2.TestCase):

    """Tests for `wikidict/wikidict.py`."""

    def test_get_summary_google_found(self):
        self.assertNotEqual(None, get_summary("Google", "en"))

    def test_get_summary_not_found(self):
        self.assertEqual(None, get_summary("Something that does not exist on wikipedia and that will never exist", "en"))


if __name__ == "__main__":
    unittest2.main()
