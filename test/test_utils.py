import unittest

from igv_reports.utils import resolve_relative_path

class UtilsTest(unittest.TestCase):


    def test_resolve_relative_path(self):

        # Relative path
        f = resolve_relative_path("/Users/foo/bar", "fn")
        self.assertEqual("/Users/foo/fn", f)

        # Absolute path
        f = resolve_relative_path("/Users/foo/bar", "/a/b/fn")
        self.assertEqual("/a/b/fn", f)

        # URL relative path
        f = resolve_relative_path("https://Users/foo/bar?q=p", "fn")
        self.assertEqual("https://Users/foo/fn?q=p", f)

        # URL absolute path
        f = resolve_relative_path("https://Users/foo/bar?q=p", "https://a/b/fn")
        self.assertEqual("https://a/b/fn", f)