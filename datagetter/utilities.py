from __future__ import print_function


# this should really all be stored in the data model, instead of stupidly calculated on the fly.


class Neighbourhood(object):

    def __init__(self, name, lat1, lon1, lat2, lon2):
        self.name = name
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2

    def check_point(self, lat, lon):
        if self.lat1 > lat > self.lat2 and self.lon2 > lon > self.lon1:
            return self.name


def get_cool_location_from_points(lat, lon):
    # print('received lat, lon: {0}, {1}'.format(lat, lon))

    # neighbourhoods are defined by top_left coordinate and bottom right coordinate.  Not exactly the best system,
    # but whatever, it will do the trick.  Definitions go from more specific to less specific in case there
    # are overlapping coordinates, we want the most specific.

    neighbourhood_array = []
    neighbourhood_array.append(Neighbourhood('Davie Street', 49.286323, -123.142272, 49.279492, -123.128367))
    neighbourhood_array.append(Neighbourhood('Coal Harbour', 49.292425, -123.135577, 49.287946, -123.115750))
    neighbourhood_array.append(Neighbourhood('Yaletown', 49.277056, -123.126136, 49.275768, -123.112746))
    neighbourhood_array.append(Neighbourhood('Stanley Park', 49.294720, -123.151971, 49.293433, -123.128796))
    neighbourhood_array.append(Neighbourhood('Downtown', 49.284979, -123.145619, 49.275404, -123.106910))
    neighbourhood_array.append(Neighbourhood('Strathcona', 49.284391, -123.099786, 49.272072, -123.077555))
    neighbourhood_array.append(Neighbourhood('Commercial Drive', 49.281088, -123.073779, 49.259470, -123.065196))
    neighbourhood_array.append(Neighbourhood('Kensington/CedarCottage', 49.259639, -123.096867, 49.242271, -123.057643))
    neighbourhood_array.append(Neighbourhood('W. Point Grey', 49.277896, -123.224669, 49.258070, -123.175917))
    neighbourhood_array.append(Neighbourhood('Kitsalano', 49.273089, -123.184895, 49.257770, -123.139469))
    neighbourhood_array.append(Neighbourhood('Hastings Sunrise', 49.286547, -123.103820, 49.274341, -123.033953))
    neighbourhood_array.append(Neighbourhood('Main Street', 49.271708, -123.101931, 49.233612, -123.100558))
    neighbourhood_array.append(Neighbourhood('East Van', 49.272660, -123.103476, 49.250255, -123.028632))
    neighbourhood_array.append(Neighbourhood('South Van', 49.234509, -123.201066, 49.193243, -122.967263))
    neighbourhood_array.append(Neighbourhood('West Van', 49.280892, -123.253251, 49.211189, -123.137894))
    neighbourhood_array.append(Neighbourhood('North Van', 49.344681, -123.190766, 49.301717, -123.043481))

    for each in neighbourhood_array:
        check_result = each.check_point(lat, lon)
        if check_result:
            return check_result


def get_nearby_landmark(lat, lon):
    # location data is nice, but how about nearness to stuff.. ie. skytrains, vgh, city hall, etc.
    # 3 distance metrics "really close to", "close to", "sort of close to"
    # take a location as a single point, and find the distance between that point and this point.
    # let's say... what... up to 500m or less - very close, .5-1km close, 1.5 km is sort of close to

    pass


def cleanup_media_files():
    # this is needed because of different dev environments and not wanting to commit my media dir contents.
    # if there are delisted posts, we're going to still be out of luck, but it's still better than nothing.

    from django.core.files.storage import default_storage
    from home_finder_project.settings import MEDIA_ROOT
    from data_grabber import store_images

    test = db.get_post_data(limit=False)
    missing_images_array = []

    for t in test:
        for i in t['image']:
            image_name = i.image_link.split('/')[-1]
            if not default_storage.exists(MEDIA_ROOT+'/media/'+image_name):
                print('missing the following media: {0}'.format(image_name))
                missing_images_array.append({'id': t['post'].id, 'link': [str(i.image_link)]})

    print('collected missing images, sending to DL and store function now...')
    print(missing_images_array)

    for m in missing_images_array:
        store_images(m['id'], m['link'])




if __name__ == "__main__":

    from datagetter import db_controller as db

    cleanup_media_files()


    if False:
        latitude = 49.212217
        longitude = -123.065862

        # latitude = 49.282404
        # longitude = -123.130255
        top_left = '49.291249, -123.147937'
        bottom_right = '49.276132, -123.108626'

        test = db.get_post_data(100)

        print('--------')

        for each in test:
            # print(each['post'].lat, each['post'].lon)
            print(get_cool_location_from_points(each['post'].lat, each['post'].lon))



        # result = get_cool_location_from_points(latitude, longitude)
        # print(result)
