"""Tests that verify that the `urlmatch` module functions correctly"""

import unittest
import sys

sys.path.append('../')

from urlmatch import urlmatch, BadMatchPattern

class URLMatchTest(unittest.TestCase):
    """Tests that verify that the `urlmatch module functions correctly"""

    def setUp(self):
        pass

    def test_invalid_scheme(self):
        """
        Tests that an invalid scheme raises a `BadMatchPattern` exception.
        """

        with self.assertRaises(BadMatchPattern):
            urlmatch('bad://test.com/*', 'http://test.com')

        with self.assertRaises(BadMatchPattern):
            urlmatch('http:/test.com/*', 'http://test.com')

    def test_invalid_domain(self):
        """
        Tests that an invalid domain raises a `BadMatchPattern` exception.
        """

        with self.assertRaises(BadMatchPattern):
            urlmatch('http:///*', 'http://test.com')

        with self.assertRaises(BadMatchPattern):
            urlmatch('http://*test/*', 'http://test.com')

        with self.assertRaises(BadMatchPattern):
            urlmatch('http://sub.*.test/*', 'http://test.com')

    def test_invalid_path(self):
        """
        Tests that an invalid path raises a `BadMatchPattern` exception.
        """
        pattern = 'http://test.com'

        with self.assertRaises(BadMatchPattern):
            urlmatch(pattern, 'http://test.com')

    def test_match_all(self):
        """
        Tests that there is an all match.
        """
        pattern = "*://*/*"

        self.assertTrue(urlmatch(pattern, 'http://test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'https://test.com/'))
        self.assertTrue(urlmatch(pattern, 'https://test.com/path'))
        self.assertTrue(urlmatch(pattern, 'https://test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'http://subdomain.test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://subdomain.test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://subdomain.test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'http://other.com/'))
        self.assertTrue(urlmatch(pattern, 'http://other.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://other.com/longer/path'))


    def test_match_exact(self):
        """
        Tests that an exact match can be made.
        """
        pattern = "http://test.com/exact/path"

        self.assertTrue(urlmatch(pattern, 'http://test.com/exact/path'))

        self.assertFalse(urlmatch(pattern, 'http://test.com/inexact/path'))
        self.assertFalse(urlmatch(pattern, 'http://badtest.com/exact/path'))

    def test_match_http(self):
        """
        Tests that if it's just an http domain, we don't match any subdomains,
        but match all paths.
        """
        pattern = 'http://test.com/*'

        self.assertTrue(urlmatch(pattern, 'http://test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/longer/path'))

        self.assertFalse(urlmatch(pattern, 'http://subdomain.test.com/'))
        self.assertFalse(urlmatch(pattern, 'http://subdomain.test.com/path'))
        self.assertFalse(urlmatch(pattern, 'http://subdomain.test.com/longer/path'))

        self.assertFalse(urlmatch(pattern, 'https://test.com/'))
        self.assertFalse(urlmatch(pattern, 'https://test.com/path'))
        self.assertFalse(urlmatch(pattern, 'https://test.com/longer/path'))


    def test_match_https(self):
        """
        Tests that if it's just the https domain, we don't match any subdomains,
        but match all paths.
        """
        pattern = 'https://test.com/*'

        self.assertTrue(urlmatch(pattern, 'https://test.com/'))
        self.assertTrue(urlmatch(pattern, 'https://test.com/path'))
        self.assertTrue(urlmatch(pattern, 'https://test.com/longer/path'))

        self.assertFalse(urlmatch(pattern, 'https://subdomain.test.com/'))
        self.assertFalse(urlmatch(pattern, 'https://subdomain.test.com/path'))
        self.assertFalse(urlmatch(pattern, 'https://subdomain.test.com/longer/path'))

        self.assertFalse(urlmatch(pattern, 'http://test.com/'))
        self.assertFalse(urlmatch(pattern, 'http://test.com/path'))
        self.assertFalse(urlmatch(pattern, 'http://test.com/longer/path'))


    def tests_wildcard_scheme(self):
        """
        Tests that if we have a wildcard scheme, then it matches both http
        and https.
        """
        pattern = '*://test.com/*'

        self.assertTrue(urlmatch(pattern, 'http://test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'https://test.com/'))
        self.assertTrue(urlmatch(pattern, 'https://test.com/path'))
        self.assertTrue(urlmatch(pattern, 'https://test.com/longer/path'))


    def test_subdomains_match(self):
        """
        Tests that if it's a wildcard subdomain, we match all of the subdomains
        and the bare domain.
        """
        pattern = 'http://*.test.com/*'

        self.assertTrue(urlmatch(pattern, 'http://test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'http://subdomain.test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://subdomain.test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://subdomain.test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'http://such.subdomain.test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://such.subdomain.test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://such.subdomain.test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'http://wow.such.subdomain.test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://wow.such.subdomain.test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://wow.such.subdomain.test.com/longer/path'))


    def test_sub_subdomain_match(self):
        """
        Tests that if we have nested subdomains, it doesn't match the bare domain,
        only the correct subdomains.
        """
        pattern = 'http://*.subdomain.test.com/*'

        self.assertFalse(urlmatch(pattern, 'http://test.com/'))
        self.assertFalse(urlmatch(pattern, 'http://test.com/path'))
        self.assertFalse(urlmatch(pattern, 'http://test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'http://subdomain.test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://subdomain.test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://subdomain.test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'http://such.subdomain.test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://such.subdomain.test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://such.subdomain.test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'http://wow.such.subdomain.test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://wow.such.subdomain.test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://wow.such.subdomain.test.com/longer/path'))


    def test_path_required_false(self):
        """
        Tests that if `path_required` is set to False, then we don't need a path.
        """
        pattern = 'http://test.com'

        self.assertTrue(urlmatch(pattern, 'http://test.com/', path_required=False))
        self.assertTrue(urlmatch(pattern, 'http://test.com/path', path_required=False))
        self.assertTrue(urlmatch(pattern, 'http://test.com/longer/path', path_required=False))


    def test_fuzzy_scheme(self):
        """
        Tests that if `fuzzy_scheme` is set to True, then as long as the scheme is
        `*`, `http`, or `https`, it will match both `http` and `https`.
        """
        pattern = 'http://test.com/*'

        self.assertTrue(urlmatch(pattern, 'http://test.com/', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'http://test.com/path', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'http://test.com/longer/path', fuzzy_scheme=True))

        self.assertTrue(urlmatch(pattern, 'https://test.com/', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'https://test.com/path', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'https://test.com/longer/path', fuzzy_scheme=True))

        pattern = 'https://test.com/*'

        self.assertTrue(urlmatch(pattern, 'http://test.com/', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'http://test.com/path', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'http://test.com/longer/path', fuzzy_scheme=True))

        self.assertTrue(urlmatch(pattern, 'https://test.com/', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'https://test.com/path', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'https://test.com/longer/path', fuzzy_scheme=True))

        pattern = '*://test.com/*'

        self.assertTrue(urlmatch(pattern, 'http://test.com/', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'http://test.com/path', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'http://test.com/longer/path', fuzzy_scheme=True))

        self.assertTrue(urlmatch(pattern, 'https://test.com/', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'https://test.com/path', fuzzy_scheme=True))
        self.assertTrue(urlmatch(pattern, 'https://test.com/longer/path', fuzzy_scheme=True))


    def test_multiple(self):
        """
        Tests that multiple patterns can be passed in as a `list` or a comma
        seperated `str` and they will be handled.
        """
        pattern = ('http://test.com/*', 'http://example.com/*')

        self.assertTrue(urlmatch(pattern, 'http://test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'http://example.com/'))
        self.assertTrue(urlmatch(pattern, 'http://example.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://example.com/longer/path'))

        self.assertFalse(urlmatch(pattern, 'http://bad.com/'))
        self.assertFalse(urlmatch(pattern, 'http://bad.com/path'))
        self.assertFalse(urlmatch(pattern, 'http://bad.com/longer/path'))

        pattern = "http://test.com/*, http://example.com/*"

        self.assertTrue(urlmatch(pattern, 'http://test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://test.com/longer/path'))

        self.assertTrue(urlmatch(pattern, 'http://example.com/'))
        self.assertTrue(urlmatch(pattern, 'http://example.com/path'))
        self.assertTrue(urlmatch(pattern, 'http://example.com/longer/path'))

        self.assertFalse(urlmatch(pattern, 'http://bad.com/'))
        self.assertFalse(urlmatch(pattern, 'http://bad.com/path'))
        self.assertFalse(urlmatch(pattern, 'http://bad.com/longer/path'))


    def test_http_auth(self):
        pattern = ('http://test.com/')

        self.assertTrue(urlmatch(pattern, 'http://user@test.com/'))
        self.assertTrue(urlmatch(pattern, 'http://user:test@test.com/'))

        self.assertIsNone(urlmatch(pattern, 'http://user:@test.com/'))
        self.assertIsNone(urlmatch(pattern, 'http://:@test.com/'))
        self.assertIsNone(urlmatch(pattern, 'http://@test.com/'))
        self.assertIsNone(urlmatch(pattern, 'http://user.test:@test.com/'))
        self.assertIsNone(urlmatch(pattern, 'http://user.test:password@test.com/'))







