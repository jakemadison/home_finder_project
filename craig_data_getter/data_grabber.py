from __future__ import print_function
import feedparser



def find_links(url):
    result = feedparser.parse(url)

    l = [str(item['dc_source']) for item in result["items"]]

    print(l)

    # at this point, we should do a check vs the db on most recent, and import new ones..





if __name__ == '__main__':

    source_url = 'http://vancouver.craigslist.ca/search/van/apa?hasPic=1&maxAsk=1600&minAsk=400&format=rss'
    # result_content, result_encoding = grab_listings(source_url)
    find_links(source_url)