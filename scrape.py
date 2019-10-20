from comment_scrape import scrape_page
import argparse
import validators
import sys
from colorama import Fore, init

"""Sample Driver for the Comment Scrape Library."""

# Global Args for file output / color

USE_COLOR = False

ascii_art = """<!--
 _____                                      _   _____                                
/  __ \                                    | | /  ___|                               
| /  \/ ___  _ __ ___  _ __ ___   ___ _ __ | |_\ `--.  ___ _ __ __ _ _ __   ___ _ __ 
| |    / _ \| '_ ` _ \| '_ ` _ \ / _ \ '_ \| __|`--. \/ __| '__/ _` | '_ \ / _ \ '__|
| \__/\ (_) | | | | | | | | | | |  __/ | | | |_/\__/ / (__| | | (_| | |_) |  __/ |   
 \____/\___/|_| |_| |_|_| |_| |_|\___|_| |_|\__\____/ \___|_|  \__,_| .__/ \___|_|   
 v0.01 An extremely limited version.                                | |              
                                                                    |_|        -->"""


def wrap_print(print_string: str, color="Fore.WHITE"):
    """Wraps the print function and adds colors, will later be used for everything"""
    if USE_COLOR:
        # TODO fix eval, it's all trusted input. But still.
        print(f'{eval(color)}{print_string}{Fore.RESET}')
    else:
        print(print_string)


if __name__ == '__main__':
    # Parse and set args
    parser = argparse.ArgumentParser(description='Crawls a page/site and returns important HTML comments.')

    parser.add_argument("-q", "--quiet", help="Silences header art and row names", action="store_true")
    parser.add_argument("-t", "--target", help="Enter a target URL to start the scan")
    parser.add_argument("-c", "--color", help="Nice colors, what's not to love?", action="store_true")

    # Future Features
    # parser.add_argument("-r", "--rank-results", help="Returns the found comments, ranked by potential")
    # parser.add_argument("-o", "--out-file", help="Stores the results of operation in a text file")
    # parser.add_argument("-s", "--show-source", help="Shows the url source page for each comment", action="store_true")
    # parser.add_argument("-i", "--interactive", help="Interactive mode")

    args = parser.parse_args()

    USE_COLOR = args.color

    # Windows printing support for Colorama
    init()

    if args.target:
        if validators.url(args.target):
            entry = args.target
        else:
            wrap_print("Could not parse URL for -t/--target", color="Fore.RED")
            wrap_print("Exiting...", color="Fore.RED")
            sys.exit(1)

    if not args.quiet:
        wrap_print(f'{ascii_art}', color="Fore.BLUE")

    if not args.target:
        while True:
            entry = input("Enter a web page to scrape for comments: ")
            if not validators.url(entry):
                wrap_print("Error parsing URL. Try Again.", color="Fore.RED")
                continue
            else:
                break

    results = scrape_page.return_page_comments(entry)
    for result in results:
        wrap_print(f'{result}', color="Fore.GREEN")

    # TODO Work out how to display findings, HI -> Low / By category of match?

    pass
