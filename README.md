[![Build Status](https://travis-ci.org/jessepollak/urlmatch.svg?branch=master)](https://travis-ci.org/jessepollak/urlmatch)

urlmatch - fnmatch for the web
========

Use `urlmatch` to verify that URLs conform to certain patterns. The library and match patterns are based heavily on the [Google Chrome Extension match patterns](http://developer.chrome.com/extensions/match_patterns).

## Usage

```python
from urlmatch import urlmatch

match_pattern = 'http://*.example.com/*'

urlmatch(match_pattern, 'http://subdomain.example.com/') # True
urlmatch(match_pattern, 'http://sub.subdomain.example.com/') # True

urlmatch(match_pattern, 'https://example.com/') # False
urlmatch(match_pattern, 'http://bad.com/') # False
```

## Options

There are a few options that affect how the match patterns work.

* `path_required` (default is True) - a `bool` which dictates whether the match pattern must have path
* `fuzzy_scheme` (default is False) - a `bool` which dictates whether the scheme should be matched "fuzzily." if this is true, then any valid scheme (`*`, `http`, `https`) will match both `http` and `https`
* `http_auth_allowed` (default is True) - `bool` which dictates whether URLs with HTTP Authentication in the URL should be allowed or not

## Match pattern syntax

The basic match pattern syntax is simple:

```
<url-pattern> := <scheme>://<host><path>
<scheme> := '*' | 'http' | 'https'
<host> := '*' | '*.' <any char except '/' and '*'>+
<path> := '/' <any chars>
```

### Examples

* `http://*/*` - matches any URL that uses the http scheme
* `https://*/*` - matches any URL that uses the https scheme
* `http://*/test*` - matches any URL that uses the http scheme and has a path that starts with `test`
* `*://test.com/*` - matches any url with the domain `test.com`
* `http://*.test.com` - matches `test.com` and any subdomain of `test.com`
* `http://test.com/foo/bar.html` - matches the exact URL


Bugs
----

If you find an issue, let me know in the issues section!

Contributing
------------

From the [Rubinius](http://rubini.us/) contribution page:

> Writing code and participating should be fun, not an exercise in
> perseverance. Stringent commit polices, for whatever their other
> qualities may bring, also mean longer turnaround times.

Submit a patch and once it's accepted, you'll get commit access to the
repository. Feel free to fork the repository and send a pull request,
once it's merged in you'll get added. If not, feel free to bug
[jessepollak](http://github.com/jessepollak) about it.

How To Contribute
-----------------

* Clone: `git@github.com:jessepollak/urlmatch.git`
* Create a topic branch: `git checkout -b awesome_feature`
* Commit away (and add unit tests for any code your write).
* Keep up to date: `git fetch && git rebase origin/master`.
* Run the tests: `python setup.py test`

Once you're ready:

* Fork the project on GitHub
* Add your repository as a remote: `git remote add your_remote your_repo`
* Push up your branch: `git push your_remote awesome_feature`
* Create a Pull Request for the topic branch, asking for review.

Once it's accepted:

* If you want access to the core repository feel free to ask! Then you
can change origin to point to the Read+Write URL:

```
git remote set-url origin git@github.com:jessepollak/urlmatch.git
```

Otherwise, you can continue to hack away in your own fork.

