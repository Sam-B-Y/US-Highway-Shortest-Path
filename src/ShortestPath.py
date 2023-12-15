import csv
from GraphProcessor import GraphProcessor
from Point import Point
from Visualize import Visualize
from pathlib import Path
import tkinter as tk
import sys
from PIL import Image, ImageTk
import tempfile
from tkinter import ttk


class ShortestPath:
    def __init__(self):
        self.myMap = {}

    def get_city_input(self, starting_city, ending_city, label_var, city_frame, root):
        if not starting_city:
            return label_var.set("Start city input is missing. Program terminated.")

        
        if not ending_city:
            return label_var.set("End city input is missing. Program terminated.")

        if not starting_city in self.myMap.keys():
            return label_var.set("Starting city not found. Please try again.")

        
        if not ending_city in self.myMap.keys():
            return label_var.set("Ending city not found. Please try again.")
    
        
        label_var.set("Loading...")
        city_frame.destroy()
        root.update()
        self.find_path(gp, viz, starting_city, ending_city, label_var, root)
        return starting_city, ending_city    

    def read_data(self, filename):
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                name = row[0] + " " + row[1]
                self.myMap[name] = Point(float(row[2]), float(row[3]))

    def user_interact(self, gp, viz):
        root = tk.Tk()
        root.title("US Highway Shortest Path")
        root.geometry("1200x400")
        label_var = tk.StringVar()
        label = tk.Label(root, textvariable=label_var)
        label.pack(pady=10)

        city_frame = tk.Frame(root)
        city_frame.pack(pady=10)

        start_label = tk.Label(city_frame, text="Enter the starting city:")
        start_label.grid(row=0, column=0, padx=5, pady=5)
        start_entry = tk.Entry(city_frame)
        start_entry.grid(row=0, column=1, padx=5, pady=5)

        end_label = tk.Label(city_frame, text="Enter the ending city:")
        end_label.grid(row=1, column=0, padx=5, pady=5)
        end_entry = tk.Entry(city_frame)
        end_entry.grid(row=1, column=1, padx=5, pady=5)

        submit_button = tk.Button(city_frame, text="Submit", command=lambda: self.get_city_input(start_entry.get(), end_entry.get(), label_var, city_frame, root))
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)
        root.mainloop()
        

    def find_path(self, gp, viz, start, end, label_var, root):
        near_start = gp.nearestPoint(self.myMap[start])
        near_end = gp.nearestPoint(self.myMap[end])

        print(f"Found {near_start} and {near_end}")

        path = gp.route(near_start, near_end)
        dist = gp.route_distance(path)

        print(f"Start: {near_start}, End: {near_end}")
        print(f"Short path has {len(path)} points.")
        print(f"Short path is {dist:.3f} in length.")
        label_var.set(f"The shortest path from: \nStart: {start} \nEnd: {end}\n is {dist:.3f} miles long.")
        plot = viz.draw_route(path)

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            plot.savefig(tmpfile.name,bbox_inches='tight')

        img = Image.open(tmpfile.name)
        img = img.resize((int(img.width / 2), int(img.height / 2)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        
        canvas = tk.Canvas(root, width=img.width(), height=img.height())
        canvas.pack()
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
        canvas.image = img
        self.canvas = canvas

        root.update()

if __name__ == "__main__":
    usa_city_file = Path(__file__).parents[1] / "data/uscities.csv"
    usa_data = [Path(__file__).parents[1] / "images/usa.png", Path(__file__).parents[1] / "data/usa.vis", Path(__file__).parents[1] / "data/usa.graph"]

    gd = ShortestPath()
    gd.read_data(usa_city_file)

    gp = GraphProcessor()
    gp.initialize(usa_data[2])
    viz = Visualize(usa_data[1], usa_data[0])
    gd.user_interact(gp, viz)
