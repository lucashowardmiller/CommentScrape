import requests
from typing import List
from comment_scrape.objects import ScrapingOperation, WebPage
from urllib.parse import urlsplit
from comment_scrape.scrape_page import get_html_comments_from_request
from bs4 import BeautifulSoup as bs
import time
"""Enumeration commands and samples"""


def start_crawl(base_url: str, max_rps=999, max_crawl=1000, obey_robots=False, user_agent="CommentScrape"):
    # Set up the crawler
    crawl = ScrapingOperation(base_url)
    crawl.domain = extract_base_domain(base_url)

    delay_after_crawl = 1 / max_rps

    # Set the crawler to use the base url as the start
    crawl.pages_to_crawl.add(base_url)

    # Set up requests headers
    headers = {
        'User-Agent': user_agent
    }

    while crawl.total_scraped < max_crawl and len(crawl.pages_to_crawl) > 0:
        # Creates a new WebPage
        current_page = WebPage(crawl.get_next_page())
        crawl.scraped_urls.add(current_page.url)

        r = requests.get(current_page.url, headers=headers)
        current_page.html_comments = get_html_comments_from_request(r)
        for link in extract_links(r):
            # Check for scope
            if extract_base_domain(link) == crawl.domain:
                if link not in crawl.scraped_urls:
                    crawl.pages_to_crawl.add(link)
        crawl.total_scraped += 1
        crawl.scraped_pages_obj.append(current_page)
        # TODO find way to factor in time for requests, will help with queues later
        time.sleep(delay_after_crawl)
    return crawl.scraped_pages_obj


def extract_base_domain(url: str) -> str:
    """Takes in a url and returns the base domain, useful for following scope"""
    return "{0.scheme}://{0.netloc}/".format(urlsplit(url))


def extract_links(request) -> List[str]:
    """Takes in a request and returns all links"""
    soup = bs(request.text, 'html.parser')
    link_tags = soup.find_all('a', href=True)
    links = []
    for link in link_tags:
        links.append(link.attrs['href'])
    return links


if __name__ == '__main__':
    start_crawl("https://543hn.com")
    pass
