from __future__ import print_function
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_finder_project.settings")
from datagetter.models import Postings, PostingImages
import django
django.setup()
from datagetter import utilities


def get_all_links():
    postings = Postings.objects.all()
    links = [p.link for p in postings]
    return links


def search_for_link(target_link):
    if target_link in get_all_links():
        return True
    else:
        return False


def get_post_data(limit=20):

    final_array = []
    if limit:
        post_array = Postings.objects.all().order_by('-post_date')[:limit]
    else:
        post_array = Postings.objects.all().order_by('-post_date')

    for each_post in post_array:
        post_item = {}
        print('each post: {0}'.format(each_post))
        lat = each_post.lat
        lon = each_post.lon

        post_item['neighbourhood'] = utilities.get_cool_location_from_points(lat, lon)

        post_item['post'] = each_post
        main_image = PostingImages.objects.filter(posting=each_post)
        post_item['image'] = main_image
        final_array.append(post_item)

    return final_array


if __name__ == "__main__":
    # link_found = search_for_link('http://test.com/')
    # print(link_found)
    data = get_post_data()
    print(data)