from comment_scrape import scrape_page
import argparse
import validators

"""Sample Driver for the Comment Scrape Library."""

# This will be good at some point
ascii_art = """Comment Scrape"""


def save_to_file():
    pass


if __name__ == '__main__':
    # Parse and set args
    parser = argparse.ArgumentParser()

    parser.add_argument("-q", "--quiet", help="Silences header art and row names",
                        action="store_true")
    parser.add_argument("-s", "--show-source", help="Shows the url source page for each comment",
                        action="store_true")
    parser.add_argument("-c", "--colors", help="Nice colors, what's not to love?",
                        action="store_true")

    # Future Features
    # parser.add_argument("-o", "--out-file", help="Stores the results of operation in a text file")


    args = parser.parse_args()

    # Scraping logic
    if not args.quiet:
        print(ascii_art)
        print("v0.01 Extremely limited version.")

    while True:
        entry = input("Enter a web page to scrape for comments: ")
        if not validators.url(entry):
            print("Error parsing URL.")
            continue
        else:
            break

    results = scrape_page.return_page_comments(entry)
    for result in results:
        print(result)
    pass
