from __future__ import print_function
import feedparser
import db_controller
import time


def create_posting_from_link(link):
    """takes in a link, follows that link, grabs the required data and sends it along to the DB"""

    print(link)


def find_links_on_page(url):

    """takes in a search url, spits out results that we can go check out later"""

    result = feedparser.parse(url)
    links = [str(item['dc_source']) for item in result["items"]]

    links.append('http://test.com/')

    for link in links:
        if db_controller.search_for_link(link):
            print("link was found in DB already: {0}".format(link))
        else:
            print("link was NOT found in DB: {0}  we should do something!".format(link))
            create_posting_from_link(link)
            time.sleep(2)  # I feel like CL might block me otherwise...

        break

    # at this point, we should do a check vs the db on most recent, and import new ones..

if __name__ == '__main__':

    source_url = 'http://vancouver.craigslist.ca/search/van/apa?hasPic=1&maxAsk=1600&minAsk=400&format=rss'
    # result_content, result_encoding = grab_listings(source_url)
    # find_links_on_page(source_url)

    test_link = 'http://vancouver.craigslist.ca/van/apa/4789342850.html'
    create_posting_from_link(test_link)