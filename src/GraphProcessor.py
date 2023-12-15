from Point import Point
from PriorityQueue import PriorityQueue
from pathlib import Path

class GraphProcessor:
    def __init__(self):
        self.myGraph = {}

    def initialize(self, file):
        self.myGraph = {}
        
        with open(file, 'r') as f:
            line = f.readline()
            inputs = line.split(" ")
            numVertices, numEdges = map(int, inputs)
            vertices = {}

            for i in range(numVertices):
                line = f.readline()
                inputs = line.split(" ")
                p = Point(float(inputs[1]), float(inputs[2]))
                self.myGraph[p] = set()
                vertices[i] = p

            for i in range(numEdges):
                line = f.readline()
                inputs = line.split(" ")
                p1, p2 = vertices[int(inputs[0])], vertices[int(inputs[1])]
                self.myGraph[p1].add(p2)
                self.myGraph[p2].add(p1)

    def nearestPoint(self, p):
        minDist = float('inf')
        minPoint = None
        for point in self.myGraph:
            dist = p.distance(point)
            if dist < minDist:
                minDist = dist
                minPoint = point
        return minPoint

    def route_distance(self, route):
        d = 0.0
        
        for i in range(len(route) - 1):
            d += route[i].distance(route[i + 1])
        return d

    def connected(self, p1, p2):
        try:
            self.route(p1, p2)
            return True
        except ValueError:
            return False

    def route(self, start, end):
        if start == end:
            raise ValueError("Start and end points are the same.")
        
        distances = {vertex: float('inf') for vertex in self.myGraph}
        previous = {vertex: None for vertex in self.myGraph}
        queue = PriorityQueue()

        distances[start] = 0
        queue.push(start, 0.0)

        while queue:
            current = queue.pop()
            current_distance = distances[current]

            if current == end:
                break

            if current_distance > distances[current]:
                continue

            for neighbor in self.myGraph[current]:
                new_distance = current_distance + current.distance(neighbor)

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
                    queue.push(neighbor, new_distance)

        if previous[end] is None:
            raise ValueError("No route found from start to end.")

        shortest_path = []
        current = end

        while current is not None:
            shortest_path.insert(0, current)
            current = previous[current]

        return shortest_path