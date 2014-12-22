from __future__ import print_function
from math import radians, cos, sin, asin, sqrt

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


class Landmark(object):

    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon

    def distance_score(self, lat, lon):

        # this should return a score (not categorical... )
        # we'll have a function that determines the best score, and uses
        # that in our description of the place.

        d = haversine(self.lon, self.lat, lon, lat)
        return d


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return km


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


def get_cool_nearby_landmark(lat, lon):

    if lat is None or lon is None:
        return None


    # location data is nice, but how about nearness to stuff.. ie. skytrains, vgh, city hall, etc.
    # 3 distance metrics "really close to", "close to", "sort of close to"
    # take a location as a single point, and find the distance between that point and this point.
    # let's say... what... up to 500m or less - very close, .5-1km close, 1.5 km is sort of close to

    landmark_array = []
    landmark_array.append(Landmark('Stanley Park', 49.293992, -123.143903))
    landmark_array.append(Landmark('Vancouver Art Gallery', 49.282894, -123.120471))
    landmark_array.append(Landmark('Science World', 49.273733, -123.102251))
    landmark_array.append(Landmark('Strathcona Park', 49.275048, -123.084999))
    landmark_array.append(Landmark('Crab Park', 49.285071, -123.101951))
    landmark_array.append(Landmark('Main & Broadway', 49.262951, -123.100878))
    landmark_array.append(Landmark('City Hall', 49.263623, -123.114868))
    landmark_array.append(Landmark('VGH', 49.261943, -123.121306))
    landmark_array.append(Landmark('Mt. St. Joseph Hospital', 49.258386, -123.095299))
    landmark_array.append(Landmark('VCC', 49.263091, -123.080536))
    landmark_array.append(Landmark('Commercial & Broadway', 49.261803, -123.069850))
    landmark_array.append(Landmark('Trout Lake', 49.255417, -123.061997))
    landmark_array.append(Landmark('Clark Park', 49.256874, -123.072125))
    landmark_array.append(Landmark('Renfrew Skytrain', 49.259254, -123.045474))
    landmark_array.append(Landmark('Queen Elizabeth Park', 49.259254, -123.045474))
    landmark_array.append(Landmark('Vandusen Gardens', 49.238356, -123.127485))
    landmark_array.append(Landmark('Granville Island', 49.270624, -123.134180))
    landmark_array.append(Landmark('UBC', 49.261271, -123.230783))
    landmark_array.append(Landmark('Deer Lake Park', 49.233901, -122.975651))
    landmark_array.append(Landmark('Robson Park', 49.258470, -123.092187))
    landmark_array.append(Landmark('Olympic Village', 49.267096, -123.115877))
    landmark_array.append(Landmark('The Naam', 49.268468, -123.167161))
    landmark_array.append(Landmark('Carnarvan Park', 49.256341, -123.171280))
    landmark_array.append(Landmark('Granville & Broadway', 49.263539, -123.138708))
    landmark_array.append(Landmark('Langara College', 49.225521, -123.108946))
    landmark_array.append(Landmark('Everett Crawley Park', 49.211562, -123.035990))
    landmark_array.append(Landmark('Mt. View Cemetary', 49.237459, -123.092896))
    landmark_array.append(Landmark("Children's Hospital", 49.245052, -123.126906))
    landmark_array.append(Landmark('Oakridge Centre', 49.232597, -123.118301))
    landmark_array.append(Landmark('Kits Beach', 49.275202, -123.153964))
    landmark_array.append(Landmark('Sunset Beach', 49.279094, -123.137914))
    landmark_array.append(Landmark('Nelson Park', 49.283070, -123.129481))
    landmark_array.append(Landmark('Robson Square', 49.281894, -123.121778))
    landmark_array.append(Landmark('Harbour Centre', 49.284665, -123.111542))
    landmark_array.append(Landmark('The Waldorf', 49.281740, -123.074657))
    landmark_array.append(Landmark('The PNE', 49.281866, -123.043328))
    landmark_array.append(Landmark('Famous Foods', 49.248748, -123.072569))
    landmark_array.append(Landmark('Park Theatre', 49.254505, -123.115020))

    current_score = 99999999
    landmark_name = None

    for each_landmark in landmark_array:
        score = each_landmark.distance_score(lat, lon)
        # print('testing landmark: {0}, score: {1}'.format(each_landmark.name, score))

        if score < current_score:
            current_score = score
            landmark_name = each_landmark.name

    # print('done testing-------')

    if landmark_name is not None:

        if current_score < .5:
            return 'very close to {0}'.format(landmark_name)
        elif current_score < 1:
            return 'near {0}'.format(landmark_name)
        elif current_score < 1.5:
            return 'kinda near {0}'.format(landmark_name)
        else:
            return None

    else:
        return None





def cleanup_media_files():
    # this is needed because of different dev environments and not wanting to commit my media dir contents.
    # if there are delisted posts, we're going to still be out of luck, but it's still better than nothing.

    from django.core.files.storage import default_storage
    from home_finder_project.settings import MEDIA_ROOT
    from data_grabber import store_images

    test = db.get_post_data(limit=False)
    missing_images_array = []

    image_total_count = 0

    for t in test:
        for i in t['image']:
            image_name = i.image_link.split('/')[-1]
            if not default_storage.exists(MEDIA_ROOT+'/media/'+image_name):
                print('missing the following media: {0}'.format(image_name))
                image_total_count += 1
                missing_images_array.append({'id': t['post'].id, 'link': [str(i.image_link)]})

    print('collected missing images, sending to DL and store function now...')
    print(missing_images_array)

    for m in missing_images_array:
        print(image_total_count, end=' -> ')
        store_images(m['id'], m['link'])
        image_total_count -= 1



if __name__ == "__main__":

    from datagetter import db_controller as db

    cleanup_media_files()


    # should be 800 meters...

    gallery = Landmark('Vancouver Art Gallery', 49.282894, -123.120471)
    print(gallery.distance_score(49.287460, -123.113799))

    landmark = get_cool_nearby_landmark(49.287460, -123.113799)
    print(landmark)




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
