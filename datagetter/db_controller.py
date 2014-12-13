from __future__ import print_function
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_finder_project.settings")
from datagetter.models import Postings, PostingImages


def get_all_links():
    postings = Postings.objects.all()
    links = [p.link for p in postings]
    return links


def search_for_link(target_link):
    if target_link in get_all_links():
        return True
    else:
        return False


def insert_posting_data(posting_data):
    # first create our posting entry, then insert our posting images, save when done all of them
    # rollback otherwise, so we don't have stranded postings, without images (that will never get added)

    pass


if __name__ == "__main__":
    link_found = search_for_link('http://test.com/')
    print(link_found)
