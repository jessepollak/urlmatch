"""
urlmatch lets you easily check whether urls are on a domain or subdomain
"""
import re

class BadMatchPattern(Exception):
    """The Exception that's raised when a match pattern fails"""
    pass

def parse_match_pattern(pattern, path_required=True, fuzzy_scheme=False):
    """
    Returns the regular expression for a given match pattern.

    Args:

        pattern: a `urlmatch` formatted match pattern
        path_required: a `bool` which dicates whether the match pattern
            must have path
        fuzzy_scheme: if this is true, then if the scheme is `*`, `http`,
            or `https`, it will match both `http` and `https`

    Returns:

        a regular expresion for the match pattern
    """
    if not isinstance(pattern, basestring):
        return

    pattern_regex = "(?:^"
    result = re.search(r'^(\*|https?):\/\/', pattern)
    if not result:
        raise BadMatchPattern("Invalid scheme: {}".format(pattern))
    elif result.group(1) == "*" or fuzzy_scheme:
        pattern_regex += "https?"
    else:
        pattern_regex += result.group(1)

    pattern_regex += "://"

    pattern = pattern[len(result.group(0)):]

    domain_and_path_regex = r'^(?:\*|(\*\.)?([^\/*]+))'
    if path_required:
        domain_and_path_regex += r'(?=\/)'

    result = re.search(domain_and_path_regex, pattern)
    if not result:
        raise BadMatchPattern("Invalid domain or path: {}".format(pattern))

    pattern = pattern[len(result.group(0)):]

    if result.group(0) == "*":
        pattern_regex += "[^/]+"
    else:
        if result.group(1):
            pattern_regex += "(?:[^/]+\\.)?"

        pattern_regex += re.escape(result.group(2))

    pattern_regex += ".*".join(map(re.escape, pattern.split("*")))
    pattern_regex += r'(\/.*)?$)'

    return pattern_regex


def urlmatch(match_pattern, url, **kwargs):
    """
    Returns whether a given match pattern matches a url

    Args:
        match_pattern: a `urlmatch` formatted match pattern_regex
        url: a url
    """
    if isinstance(match_pattern, basestring):
        match_pattern = map(str.strip, match_pattern.split(','))

    regex = "({})".format("|".join(map(lambda x: parse_match_pattern(x, **kwargs), match_pattern)))

    return regex and re.search(regex, url)


