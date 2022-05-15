# -*- coding: utf-8 -*-
"""
Created on Wed May 11 09:10:31 2022

@author: chris
"""

from tkinter import *
from tkinter import ttk
from Graphs import graphbuilder

my_graph = graphbuilder.Graph()


class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.title("Graph Builder")
        self.frames = {}

        self.frames["AddPathFrame"] = (
            AddPathFrame(parent=container, controller=self))
        self.frames["AddPathFrame"].grid(row=0, column=0, sticky="N")

        self.frames["DisplayGraphFrame"] = (
            DisplayGraphFrame(parent=container, controller=self))
        self.frames["DisplayGraphFrame"].grid(row=0, column=1, sticky="N")

        self.frames["ResultsFrame"] = (
            ResultsFrame(parent=container, controller=self))
        self.frames["ResultsFrame"].grid(row=0, column=1, sticky="N")


class AddPathFrame(Frame):
    def __init__(self, parent, controller):

        def create_path(self, *args):
            try:
                distance = float(self.path_length.get())
                my_graph.add_path(self.start_vertex.get(), self.end_vertex.get(), distance)
                controller.frames["DisplayGraphFrame"].graph_display.config(text=str(my_graph))
                self.start_vertex_box['values'] = my_graph.node_names()
                self.end_vertex_box['values'] = my_graph.node_names()
            except ValueError:
                pass
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        ttk.Label(self, text="Add a path").grid(column=0, row=0)
        ttk.Label(self, text="Start Vertex").grid(column=0, row=1)
        self.start_vertex = StringVar()
        self.start_vertex_box = ttk.Combobox(self, textvariable=self.start_vertex)
        self.start_vertex_box['values'] = my_graph.node_names()
        self.start_vertex_box.grid(column=1, row=1)

        ttk.Label(self, text="End Vertex").grid(column=0, row=2)
        self.end_vertex = StringVar()
        self.end_vertex_box = ttk.Combobox(self, textvariable=self.end_vertex)
        self.end_vertex_box['values'] = my_graph.node_names()
        self.end_vertex_box.grid(column=1, row=2)

        ttk.Label(self, text="Distance").grid(column=0, row=3)
        self.path_length = StringVar()
        self.path_length_box = ttk.Entry(self, textvariable=self.path_length)
        self.path_length_box.grid(column=1, row=3)

        self.button = ttk.Button(self, text="create path", command=create_path)
        self.button.grid(column=0, row=4, columnspan=2)


class DisplayGraphFrame(Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.graph_display = ttk.Label(self, text=str(my_graph))
        self.graph_display.grid(column=0, row=0)


class ResultsFrame(Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        self.graph_display = ttk.Label(self, text=str(my_graph))
        self.graph_display.grid(column=0, row=0)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
