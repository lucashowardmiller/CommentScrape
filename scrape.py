from comment_scrape.ranking import ingest_pages_and_rank
from comment_scrape.spider import start_crawl
from colorama import Fore, init
import argparse
import validators
import random
import sys
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
 https://github.com/lucashowardmiller/CommentScrape                 |_|        -->\n"""


def wrap_print(print_string, color=Fore.WHITE, skip=False):
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
    parser = argparse.ArgumentParser(
        description='Crawls a page/site and returns important HTML comments.')
    parser.add_argument(
        "target",
        metavar="TARGET URL",
        nargs='+',
        type=str,
        help="Enter a target URL to start the scan")
    parser.add_argument(
        "-q",
        "--quiet",
        help="Silences header art and row names",
        action="store_true")
    parser.add_argument(
        "-c",
        "--css",
        help="Show CSS Comments from <style> tags in visited pages",
        action="store_true",
        default=False)
    parser.add_argument(
        "-C",
        "--color",
        help="Nice colors, what's not to love?",
        action="store_true")
    parser.add_argument(
        "-o", "--out", help="Stores the results in a text file")
    parser.add_argument(
        "-u",
        "--ua",
        help="Sets a custom user agent.")
    parser.add_argument(
        "-s",
        "--spoof",
        help="Use a random browser user agent",
        action="store_true",
        default=False)
    parser.add_argument(
        "-i",
        "--showie",
        help="Shows IE compatibility tags, hidden by default",
        action="store_false",
        default=True)
    parser.add_argument(
        "-v",
        "--verbose",
        help="Shows additional messages",
        action="store_true",
        default=False)
    parser.add_argument(
        "-m",
        "--max",
        help="Maximum number of pages to crawl (default 500)",
        type=int,
        default=500)
    parser.add_argument(
        "-r",
        "--rps",
        help="Maximum requests per second (default 10)",
        type=int,
        default=10)


    # Future Functionality
    # parser.add_argument("-e", "--extra", help="Extra! Tests for things still being worked on, won't have nice output", action="store_true")
    # parser.add_argument("-f", "--file", help="Load a list of URLs from a file, one per line")
    # parser.add_argument("-j", "--js", help="Show JS Comments from <script> tags in visited pages")
    # spoof behavior parser.add_argument("-s", "--spoof", help="", action="store_true")
    
    
    # Windows printing support for Colorama
    init()

    args = parser.parse_args()

    if args.out:
        SAVE_TO_FILE = True
        FILE_REFERENCE = open(args.out, "w+")

    USERAGENT ="CommentScrape"

    if args.spoof:
        browser_agents = [
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        ]
        USERAGENT = random.choice(browser_agents)

    if args.rps > 0:
        MAX_RPS = args.rps
    else:
        wrap_print("-/--rps Must be greater than 0.", color=Fore.RED)
        sys.exit(1)

    # Global var setup
    TOTAL_MAX_REQUESTS = args.max
    USE_COLOR = args.color
    QUIET = args.quiet
    TARGET = args.target[0]
    CSS = args.css
    VERBOSE = args.verbose
    JS = False # future implementation

    if validators.url(TARGET):
        entry = TARGET
    else:
        wrap_print("[-] Could not parse target URL", color=Fore.RED)
        wrap_print("[-] Exiting...", color=Fore.RED)
        sys.exit(1)

    wrap_print(f'{ascii_art}', color=Fore.BLUE, skip=True)
    wrap_print(f'[+] Starting with {entry}', skip=True)

    pages = start_crawl(
        entry,
        user_agent=USERAGENT,
        max_crawl=TOTAL_MAX_REQUESTS,
        max_rps=MAX_RPS,
        css=CSS,
        js=JS,
        verbose=VERBOSE)

    wrap_print(f'[+] Done with scraping: {TARGET}', skip=True, color=Fore.CYAN)

    # Rank and display returned comments
    sorted_comments = ingest_pages_and_rank(pages, block_ie=args.showie)
    if len(sorted_comments) > 0:
        wrap_print("\nScraping Results:\n", color=Fore.CYAN, skip=True)

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
