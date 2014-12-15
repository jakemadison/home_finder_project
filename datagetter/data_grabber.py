from __future__ import print_function
import feedparser
import db_controller
import time
from bs4 import BeautifulSoup
import requests
import pickle
from datetime import datetime
import traceback
import sys
total_set = set()


def pickle_content(content):
    with open('./temp_parsed_page.data', 'wb') as pickle_file:
        pickle.dump(content, pickle_file)

    return True


def get_pickled_content():

    with open('./temp_parsed_page.data', 'r') as pickle_file:
        file_contents = pickle.load(pickle_file)

    return file_contents


def create_posting_from_parsed_link(resp):
    """takes in a link, follows that link, grabs the required data and sends it along to the DB"""

    parsed_page = BeautifulSoup(resp.content, from_encoding=resp.encoding)
    posting_title = parsed_page.find('h2', {"class": "postingtitle"})

    # get basics from the title section:
    try:
        housing_type = posting_title.find('span', {"class": 'housing'})
        if housing_type:

            price = posting_title.contents[2].strip()
            price = int(price[1:])

        housing_type = str(posting_title.contents[3].contents[0]).replace('/', '').replace('-', '').strip()
        title = posting_title.contents[4].strip()

    # get our location data:
        map_element = parsed_page.find('div', {"class": "mapbox"})

        if map_element:
            map_element = map_element.find('div', {"class": 'viewposting'})
            lat = map_element['data-latitude']
            lon = map_element['data-longitude']

        else:
            # this post has no map information
            pass

    except Exception, e:
        print('error on parsing!: {0}'.format(e))
        traceback.print_exc(file=sys.stdout)
        print(parsed_page)
        raise

    else:
        print(parsed_page)
        raise

    # get time posted:
    post_info = parsed_page.find("p", {"class": "postinginfo"}).find("time")
    posted_date = post_info['datetime'].strip()
    posted_date = datetime.strptime(posted_date[:-5], '%Y-%m-%dT%H:%M:%S')

    # get the main text of the post:
    post_body = parsed_page.find("section", {"id": "postingbody"}).text

    # get the attributes of the post, dogs, cats, washer/dryer, etc.

    # I need to find a good way to deal with these optional attributes.
    # I could just add boolean fields to the posting model, because the total number of options for what can
    # appear is fixed... so presence = 1, and absence = 0.
    # Bedroom bathroom should be numbers though...
    post_attributes = parsed_page.find("p", {"class": "attrgroup"}).findAll("span")

    post_attrs = [p.text for p in post_attributes]

    # print(post_attrs)

    for attribute in post_attributes:
        total_set.add(attribute.text)
        # print(attribute.text)

    print('--------')

    # now we need to grab all of our relevant data off of the parsed page
    #

    # then we'll send that data off to the DB to get inserted


def parse_page_from_link(link):

    """take in a link, get requests to give us the html content, parse it with beautiful soup to extract
    our required info."""

    try:
        resp = requests.get(link, timeout=3)
        resp.raise_for_status()  # <- no-op if status!=200
    except Exception, e:
        return False

    parsed_page = BeautifulSoup(resp.content, from_encoding=resp.encoding)

    # print(parsed_page.prettify(encoding=resp.encoding))

    test_data_array.append(resp)

    return parsed_page


def find_links_on_page(url):

    """takes in a search url, spits out results that we can go check out later"""

    result = feedparser.parse(url)
    links = [str(item['dc_source']) for item in result["items"]]

    # links.append('http://test.com/')

    for link in links:
        if db_controller.search_for_link(link):
            print("link was found in DB already: {0}".format(link))
        else:
            print("link was NOT found in DB: {0}  we should do something!".format(link))

            parse_page_from_link(link)
            # parsed_page = parse_page_from_link(link)
            # create_posting_from_parsed_link(parsed_page)
            print("done finding and parsing link: {0}".format(link))
            time.sleep(2)  # I feel like CL might block me otherwise...

    # at this point, we should do a check vs the db on most recent, and import new ones..

if __name__ == '__main__':

    test_data_array = []

    source_url = 'http://vancouver.craigslist.ca/search/van/apa?hasPic=1&maxAsk=1600&minAsk=400&format=rss'
    # result_content, result_encoding = grab_listings(source_url)
    # find_links_on_page(source_url)
    # pickle_content(test_data_array)

    test_link = 'http://vancouver.craigslist.ca/van/apa/4789342850.html'

    # parsed = parse_page_from_link(test_link)
    parsed_array = get_pickled_content()

    for each in parsed_array:
        try:
            create_posting_from_parsed_link(each)
        except Exception, e:
            print('dying now...')
            break

    for each in sorted(list(total_set)):
        print(each)