import csv
from GraphProcessor import GraphProcessor
from Point import Point
from Visualize import Visualize
from pathlib import Path

class ShortestPath:
    def __init__(self):
        self.myMap = {}

    def read_data(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[0] + " " + row[1]
                self.myMap[name] = Point(float(row[2]), float(row[3]))

    def user_interact(self, gp, viz):
        start = "Seattle WA"
        end = "Charlotte NC"

        if start not in self.myMap:
            print(f"Couldn't find {start} in the graph.")
            return

        if end not in self.myMap:
            print(f"Couldn't find {end} in the graph.")
            return

        near_start = gp.nearestPoint(self.myMap[start])
        near_end = gp.nearestPoint(self.myMap[end])

        print(f"Found {near_start} and {near_end}")

        path = gp.route(near_start, near_end)
        dist = gp.route_distance(path)

        print(f"Start: {near_start}, End: {near_end}")
        print(f"Short path has {len(path)} points.")
        print(f"Short path is {dist:.3f} in length.")
        viz.draw_route(path)
        
if __name__ == "__main__":
    usa_city_file = Path(__file__).parents[1] / "data/uscities.csv"
    usa_data = [Path(__file__).parents[1] / "images/usa.png", Path(__file__).parents[1] / "data/usa.vis", Path(__file__).parents[1] / "data/usa.graph"]

    gd = ShortestPath()
    gd.read_data(usa_city_file)

    gp = GraphProcessor()
    gp.initialize(usa_data[2])
    viz = Visualize(usa_data[1], usa_data[0])
    gd.user_interact(gp, viz)
