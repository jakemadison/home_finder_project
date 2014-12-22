from django.db import models


# Create your models here.

class Postings(models.Model):

    # PK is generated automatically in django.  neat!
    title = models.CharField(max_length=2024)
    link = models.URLField()

    full_text = models.TextField()

    lat = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)
    lon = models.DecimalField(max_digits=12, decimal_places=9, blank=True, null=True)

    post_date = models.DateField()
    insert_date = models.DateField(auto_now_add=True)

    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    housing_type = models.CharField(max_length=64, null=True, blank=True)

    # here's where all the posting attributes should go:
    number_bedrooms = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    number_bathrooms = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    cat_ok = models.NullBooleanField(null=True, blank=True, default=None)
    dog_ok = models.NullBooleanField(null=True, blank=True, default=None)
    furnished = models.NullBooleanField(null=True, blank=True, default=None)
    smoking = models.NullBooleanField(null=True, blank=True, default=None)
    available_date = models.DateField(null=True, blank=True)
    laundry_available = models.NullBooleanField(null=True, blank=True, default=None)
    w_d_in_unit = models.NullBooleanField(null=True, blank=True, default=None)

    delisted = models.BooleanField(default=False)

    positive_rated = models.NullBooleanField(null=True, blank=True, default=None)

    def __unicode__(self):
        return 'post instance {0} link: {1} title: {2}'.format(self.id, self.link, self.title)

    def __str__(self):
        return unicode(self).encode('utf-8')


class PostingImages(models.Model):

    posting = models.ForeignKey(Postings)
    image_data = models.ImageField(upload_to='media/', blank=True, null=True)
    image_link = models.URLField()

    def __unicode__(self):
        return 'image_id: {0}'.format(self.id)

    def __str__(self):
        return unicode(self).encode('utf-8')


class PostingRating(models.Model):
    posting = models.ForeignKey(Postings)
    positive_rating = models.NullBooleanField(null=True, blank=True, default=None)

    def __unicode__(self):
        return 'rating: {0}'.format(self.positive_rating)

    def __str__(self):
        return unicode(self).encode('utf-8')
