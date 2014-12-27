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


def get_post_data(limit=1, without_ratings=False, saved=False):

    final_array = []

    post_array = Postings.objects.all().order_by('?')

    if without_ratings:  # this is for rating of new listings.  Include delists, because we want more data.
        post_array = post_array.filter(positive_rated=None)

    if saved:
        post_array = post_array.filter(positive_rated=True)

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


def get_count_of_new_listings():
    post_count = Postings.objects.filter(positive_rated=None).count()
    save_count = Postings.objects.filter(positive_rated=True).count()
    return post_count, save_count


def delete_posting(post_id):
    print('made it to delete post with {0}'.format(post_id))
    Postings.objects.filter(id=post_id).delete()


def check_for_existing(post):
    """some real dicks love just reposting the same shit with different links and post IDs, which is going
    to skew the fuck out of our ML results."""

    # crap.  what about those marked as delisted?  Should we just consider them not delisted?
    # and then just update the link for delist checking/external linking?
    title = str(post.title)
    title_array = [str(p.title) for p in Postings.objects.all()]
    if title in title_array:
        print('same title')
        print(post.link)
        existing_full_text = Postings.objects.filter(title=title)[:1].get()
        if existing_full_text.full_text == post.full_text:
            print('BASTARDS!')
            existing_full_text.delisted = False
            existing_full_text.link = post.link
            existing_full_text.save()
            return True

    return False


if __name__ == "__main__":
    # link_found = search_for_link('http://test.com/')
    # print(link_found)
    # rate_posting(20, None)
    # data = get_post_data(without_ratings=True)
    # print(data)
    p_trial = get_post_data()
    check_for_existing(p_trial[0])