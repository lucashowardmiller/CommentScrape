"""Python classes to represent attributes about links/comments/websites"""


class WebPage:
    def __init__(self, url_entry, source_url=""):
        # What linked to this page
        self.source_url = source_url
        # The url of the page
        self.url = url_entry
        self.same_domain_links = []
        self.html_comments = []
        self.js_comments = []
        self.css_comments = []


class ScrapingOperation:
    def get_next_page(self):
        ret = self.pages_to_crawl.pop()
        while ret in self.scraped_urls:
            ret = self.pages_to_crawl.pop()
        return ret

    def __init__(self, domain: str, max_depth=5, max_crawl=100, obey_robots=False):
        self.max_depth = max_depth
        self.domain = domain
        self.obey_robots = obey_robots
        self.max_crawl = max_crawl

        self.pages_to_crawl = set()
        self.scraped_pages_obj = []
        self.scraped_urls = set()
        self.total_scraped = 0


class Comment:
    def __init__(self, comment: str, source: str):
        self.comment_text = comment
        self.predicted_value = 0
        self.source_url = source
        pass


if __name__ == '__main__':
    pass
