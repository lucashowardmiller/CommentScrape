from comment_scrape import scrape_page
import argparse
import validators
import sys
from colorama import Fore, init

"""Sample Driver for the Comment Scrape Library."""

ascii_art = """<!--
 _____                                      _   _____                                
/  __ \                                    | | /  ___|                               
| /  \/ ___  _ __ ___  _ __ ___   ___ _ __ | |_\ `--.  ___ _ __ __ _ _ __   ___ _ __ 
| |    / _ \| '_ ` _ \| '_ ` _ \ / _ \ '_ \| __|`--. \/ __| '__/ _` | '_ \ / _ \ '__|
| \__/\ (_) | | | | | | | | | | |  __/ | | | |_/\__/ / (__| | | (_| | |_) |  __/ |   
 \____/\___/|_| |_| |_|_| |_| |_|\___|_| |_|\__\____/ \___|_|  \__,_| .__/ \___|_|   
 v0.01 An extremely limited version.                                | |              
                                                                    |_|        -->"""


def save_to_file(filename: str):
    """Saves the results to a file (Formatted as text)"""
    pass


if __name__ == '__main__':
    # Parse and set args
    parser = argparse.ArgumentParser()

    parser.add_argument("-q", "--quiet", help="Silences header art and row names", action="store_true")
    parser.add_argument("-t", "--target", help="Enter a target URL to start the scan")

    # Future Features
    # parser.add_argument("-c", "--color", help="Nice colors, what's not to love?",action="store_true")
    # parser.add_argument("-r", "--rank-results", help="Returns the found comments, ranked by potential")
    # parser.add_argument("-o", "--out-file", help="Stores the results of operation in a text file")
    # parser.add_argument("-s", "--show-source", help="Shows the url source page for each comment", action="store_true")
    # parser.add_argument("-i", "--interactive", help="Interactive mode")

    args = parser.parse_args()

    if args.target:
        if validators.url(args.target):
            entry = args.target
        else:
            print("Could not parse URL for -t/--target")
            print("Exiting...")
            sys.exit(1)

    if not args.quiet:
        print(ascii_art)

    if not args.target:
        while True:
            entry = input("Enter a web page to scrape for comments: ")
            if not validators.url(entry):
                print("Error parsing URL. Try Again.")
                continue
            else:
                break

    results = scrape_page.return_page_comments(entry)
    for result in results:
        print(result)

    # TODO Work out how to display findings, HI -> Low / By category of match?

    pass
