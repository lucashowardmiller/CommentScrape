from comment_scrape import scrape_page

"""Sample Driver for the Comment Scrape Library."""

# This will be good at some point
ascii_art = """Comment Scrape"""

if __name__ == '__main__':
    print("Only grabs comments for now.")
    # add validation
    # add spider functionality
    entry = input("Enter a web page to scrape for comments: ")
    results = scrape_page.return_page_comments(entry)
    for result in results:
        print(result)
    pass
