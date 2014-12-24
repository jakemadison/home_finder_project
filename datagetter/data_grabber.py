from __future__ import print_function
import feedparser
import db_controller
import time
from bs4 import BeautifulSoup
import requests
import pickle
import re
from datetime import datetime
import traceback
import sys
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_finder_project.settings")
from datagetter.models import Postings, PostingImages
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import django
django.setup()


total_set = set()


def pickle_content(content):
    with open('./temp_parsed_page.data', 'wb') as pickle_file:
        pickle.dump(content, pickle_file)

    return True


def get_pickled_content():

    with open('./temp_parsed_page.data', 'r') as pickle_file:
        file_contents = pickle.load(pickle_file)

    return file_contents


def create_posting_from_parsed_link(resp, skip_db=False):
    """takes in a link, follows that link, grabs the required data and sends it along to the DB"""

    new_posting = Postings()

    parsed_page = BeautifulSoup(resp.content, from_encoding=resp.encoding)
    posting_title = parsed_page.find('h2', {"class": "postingtitle"})

    new_posting.link = resp.url

    # get basics from the title section:
    try:

        title = parsed_page.find('title').text.encode('utf-8')
        new_posting.title = title

        housing_type = posting_title.find('span', {"class": 'housing'})

        if housing_type:
            housing_type = housing_type.text.replace('/', '').replace('-', '').strip()
            new_posting.housing_type = housing_type

            price = posting_title.contents[2].strip()
            price = int(price[1:])
            new_posting.price = price

        else:
            # try to get price from a $ in the title:
            price = [x for x in title.split(' ') if '$' in x]

            if price:
                price = price[0]  # whatever the first one is in the list

                if '.' in price:
                    price = price.split('.')[0]

                if '/' in price:
                    price = price.split('/')[0]

                try:
                    new_posting.price = int(price[1:])  # get rid of $, and int to our object
                except ValueError, v:
                    print('could not get price.  probably a typo: {0}, {1}'.format(price, v))
                    new_posting.price = None
            else:  # still no price.. get any $ from posting title text
                price = [x for x in posting_title.text.split(' ') if '$' in x]
                if price:
                    price = price[0]  # first one in the list
                    price = price[1:]  # get rid of $
                    new_posting.price = int(price)
                else:
                    new_posting.price = None

    # get our location data:
        map_element = parsed_page.find('div', {"class": "mapbox"})

        if map_element:
            map_element = map_element.find('div', {"class": 'viewposting'})
            new_posting.lat = map_element['data-latitude']
            new_posting.lon = map_element['data-longitude']

        else:
            # this post has no map information
            pass

    except Exception, e:
        print('error on parsing!: {0}'.format(e))
        traceback.print_exc(file=sys.stdout)
        print(parsed_page)
        raise

    # get time posted:
    post_info = parsed_page.find("p", {"class": "postinginfo"}).find("time")
    posted_date = post_info['datetime'].strip()
    new_posting.post_date = datetime.strptime(posted_date[:-5], '%Y-%m-%dT%H:%M:%S')

    # get the main text of the post:
    full_text = parsed_page.find("section", {"id": "postingbody"}).text
    if full_text:
        stripped_text = os.linesep.join([s for s in full_text.splitlines() if s])
        new_posting.full_text = stripped_text.encode('utf-8')

        # if we STILL don't have price, try and get it from the full text:
        if new_posting.price is None:
            prices = [x for x in stripped_text.split(' ') if '$' in x]
            price = prices[0]
            new_posting.price = int(price[1:])

        if 'no pets' in stripped_text.lower():
            new_posting.cat_ok = False
            new_posting.dog_ok = False

        if 'no smoking' in stripped_text.lower():
            new_posting.smoking = False

    # get the attributes of the post, dogs, cats, washer/dryer, etc.
    post_attributes = parsed_page.find("p", {"class": "attrgroup"}).findAll("span")

    for attribute in post_attributes:

        attribute_text = attribute.text
        total_set.add(attribute_text)

        if 'w/d in unit' in attribute_text:
            new_posting.w_d_in_unit = True

        if 'available' in attribute_text:
            mangled_available_date = attribute_text.title()[10:]+' '+str(datetime.now().year)
            new_posting.available_date = datetime.strptime(mangled_available_date, '%b %d %Y')

        if 'no smoking' in attribute_text:
            new_posting.smoking = False

        if 'laundry in bldg' in attribute_text:
            new_posting.laundry_available = True
            new_posting.w_d_in_unit = False

        if re.compile("[0-9]BR").search(attribute_text):
            print(attribute_text)
            new_posting.number_bedrooms = int(attribute_text[0])

        if re.compile("[0-9]Ba").search(attribute_text):
            new_posting.number_bathrooms = int(attribute_text.split(' ')[-1][0])

    if skip_db:  # this is just for testing parse stuff.
        print(parsed_page)
        return new_posting

    print('--------')
    # write our record to the DB
    new_posting.save()

    # try and grab photo links:
    img_links_array = []
    script_tags = parsed_page.findAll('script')
    for each_script in script_tags:
        if 'var imgList' in each_script.text:
            var_array = [str(x) for x in each_script.text.split('"')]
            for each_var in var_array:
                if 'images.craigslist' in each_var and '50x50c' not in each_var:
                    img_links_array.append(each_var)

    if img_links_array:
        store_images(new_posting.id, img_links_array)

    print('========Done.')
    # print(parsed_page)
    #
    # raise

    # for k, v in new_posting.__dict__.iteritems():
    #     try:
    #         print("({0}) -> {1}".format(k, v))
    #     except UnicodeEncodeError, enc:
    #         print('i was unable to render this thing like an idiot {0}, {1}'.format(k.encode('utf-8')),
    #               v.encode('utf-8'))
    #     print()

    # print(parsed_page)
    # raise

    # now we need to grab all of our relevant data off of the parsed page
    #

    # then we'll send that data off to the DB to get inserted


def store_images(posting_id, img_link_array):

    """given a set of images and a posting id as a FK, download and store images"""

    for each_image_link in img_link_array:
        print('adding image: {0}'.format(each_image_link))
        new_image = PostingImages()
        new_image.image_link = each_image_link
        new_image.posting_id = posting_id

        r = requests.get(each_image_link)
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(r.content)
        img_temp.flush()

        new_image.image_data.save(each_image_link, File(img_temp))
        time.sleep(1)




def parse_page_from_link(link):

    """take in a link, get requests to give us the html content, parse it with beautiful soup to extract
    our required info."""

    resp = None

    try:
        resp = requests.get(link, timeout=5)
        resp.raise_for_status()  # <- no-op if status!=200
    except Exception, e:
        if resp and resp.status_code == 404:
            return 'delisted'  # this is going to cause problems...

        print('i died while parsing the link :<', e)
        return False

    # test_data_array.append(resp)

    return resp


def find_links_on_page(url):

    """takes in a search url, spits out results that we can go check out later"""

    result = feedparser.parse(url)
    links = [str(item['dc_source']) for item in result["items"]]

    return links

    # at this point, we should do a check vs the db on most recent, and import new ones..


def check_if_delisted(link):
    print('received link: {0}'.format(link))
    resp = parse_page_from_link(link)

    if resp == 'delisted':
        return True

    parsed_page = BeautifulSoup(resp.content, from_encoding=resp.encoding)
    removal = parsed_page.find('span', {'id': 'has_been_removed'})

    if removal:
        return True
    else:
        return False


def clean_up_delistings():
    qry = Postings.objects.filter(delisted=False).all()
    all_links = [x.link for x in qry]

    for each in all_links:
        print('testing link: {0}  ->'.format(each), end='')
        if check_if_delisted(each):
            print('posting has been detected as removed')
            qry = Postings.objects.filter(link=each).first()
            qry.delisted = True
            qry.save()
        else:
            print('still active.')

        time.sleep(1)

    print('all done.')


if __name__ == '__main__':

    test_data_array = []

    source_url = 'http://vancouver.craigslist.ca/search/van/apa?hasPic=1&maxAsk=1600&minAsk=400&format=rss'
    # result_content, result_encoding = grab_listings(source_url)
    # find_links_on_page(source_url)
    # pickle_content(test_data_array)


    # clean_up_delistings()

    if False:
        test_url = 'http://vancouver.craigslist.ca/van/apa/4799896001.html'
        p_page = parse_page_from_link(test_url)
        post_obj = create_posting_from_parsed_link(p_page, skip_db=True)

        for k, v in post_obj.__dict__.iteritems():
            print('{0} -> {1}'.format(k, v))
            print()

    if True:
        test_link = 'http://vancouver.craigslist.ca/van/apa/4789342850.html'
        link_array = find_links_on_page(source_url)
        existing_links = db_controller.get_all_links()

        print(link_array)

        for each_link in link_array:
            if each_link in existing_links:
                print('link is already there')
                continue

            print('it"s a whole new link! attempting to parse: {0}'.format(each_link))
            link_response = parse_page_from_link(each_link)
            time.sleep(1)
            create_posting_from_parsed_link(link_response)

    # parsed = parse_page_from_link(test_link)
    # parsed_array = get_pickled_content()

    # for each in parsed_array:
    #     if each.url not in existing_links:
    #         try:
    #             create_posting_from_parsed_link(each)
    #         except Exception, e:
    #             traceback.print_exc(file=sys.stdout)
    #             print('dying now...')
    #             break
    #
    #     else:
    #         print('link exists, skipping: {0}'.format(each.url))
    #
    # for each in sorted(list(total_set)):
    #     print(each)