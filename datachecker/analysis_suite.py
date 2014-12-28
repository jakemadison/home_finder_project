from __future__ import print_function
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from numpy import genfromtxt, savetxt
from sklearn import datasets, metrics
import os
import numpy as np
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_finder_project.settings")
import django
django.setup()
from datagetter import models
from django.forms.models import model_to_dict


def get_appropriate_model():

    data_fields = ['lat', 'lon', 'price', 'number_bathrooms', 'number_bedrooms',
                   'cat_ok', 'dog_ok', 'furnished', 'smoking', 'laundry_available',
                   'w_d_in_unit']

    formats = ['f', 'f', 'f', 'i', 'i', 'b', 'b', 'b', 'b', 'b', 'b']

    dtype = dict(names=data_fields, formats=formats)

    qry = models.Postings.objects.all()
    q_dict_list = []

    for q in qry:
        q_dict_list.append(model_to_dict(q, fields=data_fields))

    print(q_dict_list)

    values = tuple(q_dict_list[name] for name in data_fields)
    header_array = np.array(values, dtype=dtype)

    print(header_array)




def turn_model_into_dataset():
    qry = models.Postings.objects.all()
    vlqs = qry.values_list()
    target = [str(f.name) for f in models.Postings._meta.fields]
    print(target)

    return target


def random_forrest(dataset=None):

    print('i"m in a random forrest!')

    if dataset is None:
        dataset = datasets.load_iris()

    print(type(dataset))
    # fit a CART model to the data
    model = DecisionTreeClassifier()
    model.fit(dataset.data, dataset.target)
    # print(model)
    # make predictions
    expected = dataset.target
    predicted = model.predict(dataset.data)
    # summarize the fit of the model
    # print(metrics.classification_report(expected, predicted))
    # print(metrics.confusion_matrix(expected, predicted))

    print(type(dataset.data))
    print(dataset.target_names)

    return


if __name__ == "__main__":
    get_appropriate_model()
    # data = turn_model_into_dataset()
    # random_forrest()