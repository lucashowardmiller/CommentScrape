from bs4 import BeautifulSoup as bs
from bs4 import Comment as comment
from typing import List
import requests
import re

"""Scraping functions for finding comments"""

# Regex for CSS/JS Comments
css_re = re.compile(r'/\*.+?\*/', re.DOTALL)
js_re = re.compile(r'//*/', re.DOTALL)

def get_html_comments(r) -> List[str]:
    """Get HTML comments from a request object"""
    soup = bs(r.text, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, comment))
    return comments

def get_css_comments(r) -> List[str]:
    """Get CSS comments from a request object"""
    return re.findall(css_re, r.text)

def get_js_comments(r) -> List[str]:
    """Get JS comments from a request object"""
    return re.findall(js_re, r.text)
    

