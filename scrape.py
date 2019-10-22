from comment_scrape.ranking import ingest_pages_and_rank
from comment_scrape.spider import start_crawl, extract_base_domain
import argparse
import validators
import random
import sys
from colorama import Fore, init

"""Sample Driver for the Comment Scrape Library."""

# Global Args for color / file output / quiet
USE_COLOR = False
SAVE_TO_FILE = False
FILE_REFERENCE = ""
QUIET = False

ascii_art = """<!--
 _____                                      _   _____                                
/  __ \                                    | | /  ___|                               
| /  \/ ___  _ __ ___  _ __ ___   ___ _ __ | |_\ `--.  ___ _ __ __ _ _ __   ___ _ __ 
| |    / _ \| '_ ` _ \| '_ ` _ \ / _ \ '_ \| __|`--. \/ __| '__/ _` | '_ \ / _ \ '__|
| \__/\ (_) | | | | | | | | | | |  __/ | | | |_/\__/ / (__| | | (_| | |_) |  __/ |   
 \____/\___/|_| |_| |_|_| |_| |_|\___|_| |_|\__\____/ \___|_|  \__,_| .__/ \___|_|   
 v1.00 It mostly works!                                             | |              
                                                                    |_|        -->"""


def wrap_print(print_string: str, color=Fore.WHITE, skip=False):
    """Wraps the print function and adds colors, will later be used for everything"""
    if skip and QUIET:
        return
    if SAVE_TO_FILE and not skip:
        FILE_REFERENCE.write(f'{print_string}\n')
    if USE_COLOR:
        print(f'{color}{print_string}{Fore.RESET}')
    else:
        print(print_string)


if __name__ == '__main__':
    # Parse and set args
    parser = argparse.ArgumentParser(description='Crawls a page/site and returns important HTML comments.')

    parser.add_argument("-q", "--quiet", help="Silences header art and row names", action="store_true")
    parser.add_argument("-t", "--target", help="Enter a target URL to start the scan")
    parser.add_argument("-c", "--color", help="Nice colors, what's not to love?", action="store_true")
    parser.add_argument("-o", "--out", help="Stores the results of operation in a text file")
    parser.add_argument("-u", "--useragent", help="Set a custom user agent. Uses \"CommentScrape\" by default", default="CommentScrape")
    parser.add_argument("-s", "--spoof", help="Sets a browser user agent. In the future, behavior.", action="store_true")
    parser.add_argument("-i", "--showie", help="Shows IE compatibility tags, hidden by default", action="store_false", default=True)
    parser.add_argument("-m", "--max", help="Maximum number of pages to crawl. Default 500", type=int, default=500)
    parser.add_argument("-r", "--rps", help="Max number of Requests Per Second", type=int, default=10)
    parser.add_argument("-p", "--progress", help="Adds a progress report every ten percent", action="store_true", default=False)

    # Future Functionality
    # parser.add_argument("-e", "--extra", help="Extra! Tests for things still being worked on, won't have nice output", action="store_true")
    # parser.add_argument("-f", "--file", help="Load a list of URLs from a file, one per line")
    # parser.add_argument("-c", "--css", help="Show CSS Comments from <style> tags in visited pages")
    # parser.add_argument("-j", "--js", help="Show JS Comments from <script> tags in visited pages")

    args = parser.parse_args()

    # Global var setup
    if args.out:
        SAVE_TO_FILE = True
        FILE_REFERENCE = open(args.out, "w+")

    if args.spoof:
        browser_agents = ["Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
                          "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0",
                          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"]
        USERAGENT = random.choice(browser_agents)

    if args.rps > 0:
        MAX_RPS = args.rps
    else:
        wrap_print("-/--rps Must be greater than 0.", color=Fore.RED)
        sys.exit(1)

    TOTAL_MAX_REQUESTS = args.max
    MAX_RPS = args.rps
    USE_COLOR = args.color
    QUIET = args.quiet
    USERAGENT = args.useragent
    PROGRESS_BAR = args.progress

    # Windows printing support for Colorama
    init()

    if args.target:
        if validators.url(args.target):
            entry = args.target
        else:
            wrap_print("Could not parse URL for -t/--target", color=Fore.RED)
            wrap_print("Exiting...", color=Fore.RED)
            sys.exit(1)

    wrap_print(f'{ascii_art}', color=Fore.BLUE, skip=True)

    if not args.target:
        while True:
            entry = input("Enter a web site to scrape for comments: ")
            if not validators.url(entry):
                wrap_print("Error parsing URL. Try Again.", color=Fore.RED)
                continue
            else:
                break

    wrap_print(f'Starting with {entry}', skip=True)

    pages = start_crawl(entry, user_agent=USERAGENT, max_crawl=TOTAL_MAX_REQUESTS, max_rps=MAX_RPS, print_progress=PROGRESS_BAR)

    wrap_print(f'Done with scraping: {extract_base_domain(entry)}', skip=True)

    # Rank and display returned comments
    sorted_comments = ingest_pages_and_rank(pages, block_ie=args.showie)
    if len(sorted_comments) > 0:
        wrap_print("Scraping Results:", color=Fore.CYAN, skip=True)

        for ranked_comment in sorted_comments:
            if ranked_comment.predicted_value > 10:
                ccolor = Fore.GREEN
            elif ranked_comment.predicted_value > 5:
                ccolor = Fore.LIGHTGREEN_EX
            else:
                ccolor = Fore.LIGHTYELLOW_EX

            if len(ranked_comment.all_urls) == 0:
                wrap_print(f'|{int(ranked_comment.predicted_value)}|{ranked_comment.comment_text}| {ranked_comment.source_url} ||', color=ccolor)
            else:
                wrap_print(f'|{int(ranked_comment.predicted_value)}|{ranked_comment.comment_text}| {ranked_comment.source_url} | Found on {len(ranked_comment.all_urls) - 1} other pages. |', color=ccolor)
    else:
        wrap_print("Nothing found :(", skip=True, color=Fore.LIGHTRED_EX)

    # Cleanup
    if SAVE_TO_FILE:
        FILE_REFERENCE.close()
    pass
