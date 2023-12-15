import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class Visualize:
    RADIUS = 6378137.0 # in meters on the equator
    NODE_SIZE = 35
    EDGE_SIZE = 1

    def __init__(self, visFile, imageFile):
        self.myImageFileName = imageFile
        self.read_vis(visFile)
        self.set_up()

    def draw_point(self, p, color='blue'):
        x_pixel, y_pixel = self.convert_coordinates_to_pixels(p)
        plt.scatter(x_pixel, y_pixel, s=self.NODE_SIZE, c=color, marker='o')
    
    def draw_edge(self, u, v):
        u_pixel = self.convert_coordinates_to_pixels(u)
        v_pixel = self.convert_coordinates_to_pixels(v)
        plt.plot([u_pixel[0],  v_pixel[0]], [u_pixel[1],  v_pixel[1]], color='blue', linewidth=self.EDGE_SIZE)
    
    def draw_graph(self, vertices, edges):
        for p in vertices:
            self.draw_point(p)
        for edge in edges:
            self.draw_edge(edge[0], edge[1])
    
    def draw_route(self, route):
        if route is None or len(route) == 0:
            return
        prev = route[0]
        self.draw_point(prev)
        for i in range(1, len(route)):
            next = route[i]
            self.draw_edge(prev, next)
            prev = next
        self.draw_point(route[0], 'green')
        self.draw_point(route[-1], 'red')
        plt.show()
    
    def read_vis(self, visFile):
        with open(visFile, "r") as f:
            lonBounds = f.readline().split(" ")
            self.myMinLongitude = float(lonBounds[0])
            self.myMaxLongitude = float(lonBounds[1])

            latBounds = f.readline().split(" ")
            self.myMinLatitude = float(latBounds[0])
            self.myMaxLatitude = float(latBounds[1])

            visDims = f.readline().split(" ")
            self.myWidth = int(visDims[0])
            self.myHeight = int(visDims[1])
    
    def set_up(self):
        img = mpimg.imread(self.myImageFileName)
        plt.figure(figsize=(img.shape[1] / 100, img.shape[0] / 100))
        plt.imshow(img)
        plt.axis('off')
        
    
    def draw_pointSet(self, points):
        for p in points:
            self.draw_point(p)

    def lat2y(self, aLat):
        return math.log(math.tan(math.pi / 4 + math.radians(aLat) / 2)) * self.RADIUS

    def convert_coordinates_to_pixels(self, point):
        x_ratio = (point.lon - self.myMinLongitude) / (self.myMaxLongitude - self.myMinLongitude)
        y_ratio = (self.lat2y(point.lat) - self.lat2y(self.myMinLatitude)) / (self.lat2y(self.myMaxLatitude) - self.lat2y(self.myMinLatitude))
        x_pixel = x_ratio * self.myWidth
        y_pixel = (1 - y_ratio) * self.myHeight

        return x_pixel, y_pixel
