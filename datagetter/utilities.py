from __future__ import print_function


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
    print('received lat, lon: {0}, {1}'.format(lat, lon))

    neighbourhood_array = []
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


if __name__ == "__main__":
    latitude = 49.212217
    longitude = -123.065862

    # latitude = 49.282404
    # longitude = -123.130255
    top_left = '49.291249, -123.147937'
    bottom_right = '49.276132, -123.108626'

    result = get_cool_location_from_points(latitude, longitude)
    print(result)


