"""Tests that verify that the `urlmatch` module functions correctly"""

import unittest
import sys

sys.path.append('../')

from urlmatch import urlmatch, BadMatchPattern


class URLMatchTest(unittest.TestCase):
    """Tests that verify that the `urlmatch module functions correctly"""

    def setUp(self):
        self._http_url = 'http://test.com/'
        self._https_url = 'https://test.com/'
        self._subdomain_url = 'http://subdomain.test.com/'

    def _check_raises(self, pattern):
        """
        Check that a given pattern raises a BadMatchPattern exception.
        """
        with self.assertRaises(BadMatchPattern):
            urlmatch(pattern, self._http_url)

    def test_invalid_scheme(self):
        """
        Tests that an invalid scheme raises a `BadMatchPattern` exception.
        """
        self._check_raises('bad://test.com/*')
        self._check_raises('http:/test.com/*')

    def test_invalid_domain(self):
        """
        Tests that an invalid domain raises a `BadMatchPattern` exception.
        """
        self._check_raises('http:///*')
        self._check_raises('http://*test/*')
        self._check_raises('http://sub.*.test/*')

    def test_invalid_path(self):
        """
        Tests that an invalid path raises a `BadMatchPattern` exception.
        """
        self._check_raises('http://test.com')

    def _check_true_match(self, pattern, root_url, **kwargs):
        """Check the result of a call to urlmatch is True."""
        urls = self._build_urls(root_url)
        self._check_urls(pattern, urls, True, **kwargs)

    def _check_false_match(self, pattern, root_url, **kwargs):
        """Check the result of a call to urlmatch is False."""
        urls = self._build_urls(root_url)
        self._check_urls(pattern, urls, False, **kwargs)

    @staticmethod
    def _build_urls(root_url):
        """Given a root URL return a list of test URLs."""
        paths = ['', 'path', 'longer/path']
        return [root_url + path for path in paths]

    def _check_urls(self, pattern, urls, expected_result, **kwargs):
        """Check a list of URLs return the expected result."""
        for url in urls:
            result = urlmatch(pattern, url, **kwargs)
            self.assertEqual(result, expected_result)

    def test_match_all(self):
        """
        Tests that there is an all match.
        """
        pattern = "*://*/*"

        self._check_true_match(pattern, self._http_url)
        self._check_true_match(pattern, self._https_url)
        self._check_true_match(pattern, self._subdomain_url)
        self._check_true_match(pattern, 'http://other.com/')

    def test_match_exact(self):
        """
        Tests that an exact match can be made.
        """
        pattern = "http://test.com/exact/path"

        self.assertEqual(urlmatch(pattern, 'http://test.com/exact/path'), True)

        bad_urls = ['http://test.com/inexact/path',
                    'http://badtest.com/exact/path']
        self._check_urls(pattern, bad_urls, False)

    def test_match_http(self):
        """
        Tests that if it's just an http domain, we don't match any subdomains,
        but match all paths.
        """
        pattern = 'http://test.com/*'

        self._check_true_match(pattern, self._http_url)
        self._check_false_match(pattern, self._https_url)
        self._check_false_match(pattern, self._subdomain_url)

    def test_match_https(self):
        """
        Tests that if it's just the https domain, we don't match any
        subdomains, but match all paths.
        """
        pattern = 'https://test.com/*'

        self._check_false_match(pattern, self._http_url)
        self._check_true_match(pattern, self._https_url)
        self._check_false_match(pattern, self._subdomain_url)

    def tests_wildcard_scheme(self):
        """
        Tests that if we have a wildcard scheme, then it matches both http
        and https.
        """
        pattern = '*://test.com/*'

        self._check_true_match(pattern, self._http_url)
        self._check_true_match(pattern, self._https_url)

    def test_subdomains_match(self):
        """
        Tests that if it's a wildcard subdomain, we match all of the subdomains
        and the bare domain.
        """
        pattern = 'http://*.test.com/*'

        self._check_true_match(pattern, self._http_url)
        self._check_true_match(pattern, self._subdomain_url)
        self._check_true_match(pattern, 'http://such.subdomain.test.com/')
        self._check_true_match(pattern, 'http://wow.such.subdomain.test.com/')

    def test_sub_subdomain_match(self):
        """
        Tests that if we have nested subdomains, it doesn't match the bare
        domain, only the correct subdomains.
        """
        pattern = 'http://*.subdomain.test.com/*'

        self._check_false_match(pattern, self._http_url)
        self._check_true_match(pattern, self._subdomain_url)
        self._check_true_match(pattern, 'http://such.subdomain.test.com/')
        self._check_true_match(pattern, 'http://wow.such.subdomain.test.com/')

    def test_path_required_false(self):
        """
        Tests that if `path_required` is set to False, then we don't need a
        path.
        """
        pattern = 'http://test.com'

        self._check_true_match(pattern, self._http_url, path_required=False)

    def test_fuzzy_scheme(self):
        """
        Tests that if `fuzzy_scheme` is set to True, then as long as the scheme
        is `*`, `http`, or `https`, it will match both `http` and `https`.
        """
        pattern = 'http://test.com/*'

        self._check_true_match(pattern, self._http_url, fuzzy_scheme=True)
        self._check_true_match(pattern, self._https_url, fuzzy_scheme=True)

        pattern = 'https://test.com/*'

        self._check_true_match(pattern, self._http_url, fuzzy_scheme=True)
        self._check_true_match(pattern, self._https_url, fuzzy_scheme=True)

        pattern = '*://test.com/*'

        self._check_true_match(pattern, self._http_url, fuzzy_scheme=True)
        self._check_true_match(pattern, self._https_url, fuzzy_scheme=True)

    def test_multiple(self):
        """
        Tests that multiple patterns can be passed in as a `list` or a comma
        seperated `str` and they will be handled.
        """
        tuple_pattern = ('http://test.com/*', 'http://example.com/*')

        self._check_true_match(tuple_pattern, self._http_url)
        self._check_true_match(tuple_pattern, 'http://example.com/')
        self._check_false_match(tuple_pattern, 'http://bad.com/')

        pattern = "http://test.com/*, http://example.com/*"

        self._check_true_match(pattern, self._http_url)
        self._check_true_match(pattern, 'http://example.com/')
        self._check_false_match(pattern, 'http://bad.com/')

    def test_http_auth(self):
        """
        Tests for URLs containing HTTP Authentication.
        """
        pattern = ('http://test.com/')

        good_urls = ['http://user@test.com/', 'http://user:test@test.com/']
        self._check_urls(pattern, good_urls, expected_result=True)

        bad_urls = ['http://user:@test.com/', 'http://:@test.com/',
                    'http://@test.com/', 'http://user.test:@test.com/',
                    'http://user.test:password@test.com/']
        self._check_urls(pattern, bad_urls, expected_result=False)
