from __future__ import print_function
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_finder_project.settings")
from datagetter.models import Postings, PostingImages, PostingRating
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


def get_post_data(limit=10, without_ratings=False):

    final_array = []

    post_array = Postings.objects.all().order_by('?')

    if without_ratings:
        post_array = post_array.filter(positive_rated=None)

    if limit:
        post_array = post_array[:limit]

    for each_post in post_array:
        post_item = {}
        print('each post: {0}'.format(each_post))
        lat = each_post.lat
        lon = each_post.lon

        post_item['neighbourhood'] = utilities.get_cool_location_from_points(lat, lon)
        post_item['landmark'] = utilities.get_cool_nearby_landmark(lat, lon)

        post_item['post'] = each_post
        main_image = PostingImages.objects.filter(posting=each_post)
        post_item['image'] = main_image
        final_array.append(post_item)

    return final_array


def rate_posting(post_id, liked):
    post = Postings.objects.filter(id=int(post_id))[:1].get()
    print(post)
    post.positive_rated = liked
    post.save()

    rating_record = PostingRating()
    rating_record.posting_id = int(post_id)
    rating_record.positive_rating = liked
    rating_record.save()


if __name__ == "__main__":
    # link_found = search_for_link('http://test.com/')
    # print(link_found)
    # rate_posting(20, None)
    data = get_post_data(without_ratings=True)
    print(data)