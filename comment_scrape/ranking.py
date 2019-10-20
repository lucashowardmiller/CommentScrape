"""Functions that take in an input, and return an approximation of how neat it might be"""

import re
import collections
import math

keywords = ['usr', 'user', 'pass', 'admin', 'TODO', 'backup', 'api', 'key']

# Compiles a regex that will match any string in the keyword list
keyword_regex = re.compile("(?=("+'|'.join(keywords)+r"))", re.IGNORECASE)

# I might have a wrapper function in the future that sums all of these, or picks the highest


def shannon_entropy_rank(comment: str) -> int:
    """Returns an int 0-10, of how random a string is. Designed to find api keys and randomly generated strings"""
    # Original code stolen from https://stackoverflow.com/a/47348423, thanks.
    probabilities = [n_x / len(comment) for x, n_x in collections.Counter(comment).items()]
    e_x = [-p_x * math.log(p_x, 2) for p_x in probabilities]
    # Shannon works better on longer strings
    return sum(e_x) * 2


def keywords_rank(comment: str) -> int:
    """Returns an int 0-10+, of if the string matches one or more keywords"""
    # I don't have a great way of knowing what ones matter more so it returns ten on each match
    results = re.findall(keyword_regex, comment)

    if results:
        return len(results) * 10
    else:
        return 0


def encoding_rank(comment: str) -> int:
    """Returns an int 0-10+ of if the comment looks like valid base64"""
    pass


if __name__ == '__main__':
    pass