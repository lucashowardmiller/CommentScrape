"""Functions that take in an input, and return an approximation of how neat it might be"""

import re

keywords = "usr, user, pass, admin, TODO, backup, api, key"

# re.compile(keywords, re.IGNORECASE)


def shannon_entropy_rank():
    """Returns an int 0-10, of how random a string is. Designed to find api keys and randomly generated strings"""
    pass


def keywords_rank():
    """Returns an int 0-10+, of if the string matches one or more keywords"""
    pass


def encoding_rank():
    """Returns an int 0-10 of if the comment looks like valid base64"""
    pass


if __name__ == '__main__':
    pass