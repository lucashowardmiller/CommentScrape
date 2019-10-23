from comment_scrape.objects import ScrapingOperation, WebPage
from comment_scrape.scrape_page import get_html_comments, get_css_comments
from bs4 import BeautifulSoup as bs
from urllib.parse import urlsplit
from typing import List
import requests
import time

"""Spidering functions"""


def start_crawl(base_url: str, max_rps=9999, max_crawl=1000, obey_robots=False, user_agent="CommentScrape", print_progress=False, css=False, js=False, verbose=False):
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
        # You may not like it, but this is what peak exception handling looks like
        try:
            r = requests.get(current_page.url, headers=headers)
        except:
            if verbose:
                print(f'[-] Page {current_page.url} did not load correctly')

        current_page.html_comments = get_html_comments(r)
        if css:
            current_page.css_comments = get_css_comments(r)

        for link in extract_links(r, css, js):
            if check_scope(link, crawl.domain):
                if link not in crawl.scraped_urls and \
                   link not in crawl.pages_to_crawl and \
                   link not in crawl.domain:
                    if verbose:
                        print("\t[+] New in-scope page found: " + link)
                    link = create_url(link, crawl.domain)
                    crawl.pages_to_crawl.add(link)
        crawl.total_scraped += 1
        crawl.scraped_pages_obj.append(current_page)
        # TODO find way to factor in time for requests, will help with queues later
        crawl.total_scraped += 1
        time.sleep(delay_after_crawl)
    return crawl.scraped_pages_obj


def extract_base_domain(url: str) -> str:
    """Takes in a url and returns the base domain, useful for following scope"""
    return "{0.scheme}://{0.netloc}/".format(urlsplit(url))


def check_scope(url: str, domain) -> str:
    # BUG TODO make http and https match
    """Checks that link is within scope"""
    if url == "#":
        return False
    base_url = extract_base_domain(url)
    scheme = "{0.scheme}".format(urlsplit(url))
    return base_url == domain or not scheme


def create_url(url: str, domain) -> str:
    # Check if relative
    scheme = "{0.scheme}".format(urlsplit(url))
    if not scheme:
        return domain + url
    else:
        return url


def extract_links(request, css, js) -> List[str]:
    """Takes in a request and returns all links"""
    soup = bs(request.text, 'html.parser')
    anchor_tags = soup.find_all('a', href=True)
    links = []
    for link in anchor_tags:
        links.append(link.attrs['href'])
    if css:
        link_tags = soup.find_all('link', href=True)
        for link in link_tags:
            links.append(link.attrs['href'])
        style_tags = soup.find_all('style')
    if js:
        pass # todo
    return links


if __name__ == '__main__':
    start_crawl("https://543hn.com")
    pass
