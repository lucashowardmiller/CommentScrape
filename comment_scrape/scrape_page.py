from bs4 import BeautifulSoup as bs
from bs4 import Comment as comment
from typing import List
import requests
import re

"""Scraping functions for finding HTML comments"""

# Regex for CSS/JS Comments
css_re = re.compile(r'/\*.+?\*/', re.DOTALL)
js_re = re.compile(r'//*/', re.DOTALL)

def get_html_comments(url: str) -> List[str]:
    """Takes a url as an arg, and returns a list of all HTML comments""" 
    r = requests.get(url)
    soup = bs(r.text, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, comment))
    # find JS and CSS comments by browsing tree
    return comments
    
def get_css_comments(url: str) -> List[str]:
    """Takes a url as an arg, and returns a list of all HTML comments""" 
    r = requests.get(url)
    comments = re.findall(css_re, r.text)
    return comments
    
def get_js_comments(url: str) -> List[str]:
    """Takes a url as an arg, and returns a list of all HTML comments""" 
    r = requests.get(url)
    comments = re.findall(js_re, r.text)
    return comments

