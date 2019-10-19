from typing import List
import bs4
import requests
import re

"""Scraping functions for finding HTML comments"""

# A XML parser would be faster/better, but I'm not trying to blow up my tool with untrusted input

# Filters out all HTML comment tags, even if they appear in page text
html_comments = re.compile("(?s)<!--.+?-->", re.DOTALL)

# TODO regex adds
# PHP
# CSS
# More


def return_page_comments(url: str) -> List[str]:
    """Takes a url as an arg, and returns a list of all HTML comments matching the regex"""
    r = requests.get(url)
    return_comments = re.findall(html_comments, r.text)
    return return_comments


if __name__ == '__main__':
    print(return_page_comments("https://html.com/tags/comment-tag/"))