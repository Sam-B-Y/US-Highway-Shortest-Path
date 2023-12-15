from math import radians, cos, sqrt

class Point:
    EARTH_RADIUS = 3963.2

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.my_to_string = f"({lat}, {lon})"

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def distance(self, p):
        delta_lon = radians(p.get_lon() - self.lon)
        delta_lat = radians(p.get_lat() - self.lat)
        delta_x = self.EARTH_RADIUS * cos(radians((self.lat + p.get_lat()) / 2)) * delta_lon
        delta_y = self.EARTH_RADIUS * delta_lat
        return sqrt(delta_x ** 2 + delta_y ** 2)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.lat == other.get_lat() and self.lon == other.get_lon()

    def __hash__(self):
        return hash(self.lat + self.lon)

    def __str__(self):
        return self.my_to_string

    def __lt__(self, other):
        lat_comp = self.lat - other.get_lat()
        if lat_comp != 0:
            return lat_comp < 0
        return self.lon - other.get_lon() < 0

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not (self <= other)

    def __ge__(self, other):
        return not (self < other)
