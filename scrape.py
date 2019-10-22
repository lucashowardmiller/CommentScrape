from comment_scrape import scrape_page
from comment_scrape.objects import WebPage
from comment_scrape.ranking import ingest_pages_and_rank
from comment_scrape.spider import start_crawl
import argparse
import validators
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
 v0.02 An extremely limited version.                                | |              
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
    parser.add_argument("-m", "--max", help="Maximum number of pages to crawl. Default 1000")

    args = parser.parse_args()

    # Global var setup
    USE_COLOR = args.color
    QUIET = args.quiet
    if args.out:
        SAVE_TO_FILE = True
        FILE_REFERENCE = open(args.out, "w+")

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

    pages = start_crawl(entry)

    wrap_print("Done with scraping", skip=True)

    wrap_print("Scraping Results:", color=Fore.CYAN, skip=True)

    sorted_comments = ingest_pages_and_rank(pages)
    for ranked_comment in sorted_comments:
        if ranked_comment.predicted_value > 10:
            ccolor = Fore.GREEN
        elif ranked_comment.predicted_value > 5:
            ccolor = Fore.LIGHTGREEN_EX
        else:
            ccolor = Fore.LIGHTYELLOW_EX

        wrap_print(f'|{int(ranked_comment.predicted_value)}|{ranked_comment.comment_text}| {ranked_comment.source_url} |', color=ccolor)


    # Cleanup
    if SAVE_TO_FILE:
        FILE_REFERENCE.close()
    pass
