import networkx as nx
import rasterio
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt

# TODO:
# Update constructor to ensure that:
# We create elevation based on heightmap
# Update the nodes based on heat data passed in
# Create a function that actively updates the terrain graph

class TerrainGraph:

    # Class fields
    elevationImage = 0
    heatImage = 0
    elevationThreshold = 20
    graph = 0
    updateInterval = 5 # Unit in seconds

    """
    Function takes in a valid path to an image and converts it to a graph
    Requires:
        - elevationImage: image path with valid height data
        - heatMap: image path with temperature data
        - both elevationImage and heatMap are of the same width and height
    """
    def __init__(self, elevationImagePath):
        self.elevationImage = rasterio.open(elevationImagePath)
        # transform = self.elevationImage.transform
        # self.heatMap = Image.open(heatMap)
        self.graph = nx.Graph()
        

        elevation_data = self.elevationImage.read(1)

        # We take the elevation image (perlin noise format or whatever format they they give)
        # then generate the graph with each vertex having height information.
        width = self.elevationImage.width
        height = self.elevationImage.height

        # Rows along the image
        prevRow = []
        currentRow = []

        for j in range(height):
            prevCoordinate = ()
            for i in range(width):
                currCoordinate = (i, j)
                self.graph.add_node(currCoordinate)
                nx.set_node_attributes(self.graph, elevation_data[j,i], 'elevation')
                currentRow.append(currCoordinate)

                # TODO: Add appropriate edges based on the intensities on the elevationImage
                if j > 0: # Connect node from above
                    # above_neighbor = (i,j-1)
                    # elevation_diff = abs(elevation_data[j,i]-elevation_data[j-1,i])
                    # weight = dynamic_cost(elevation_diff, elevation_data[j,i],elevation_data[j-1,i])
                    self.graph.add_edge((i, j-1),currCoordinate)
                if i > 0: # Connect node from left side
                    # left_neighbor = (i-1,j)
                    # elevation_diff = abs(elevation_data[j,i]-elevation_data[j,i-1])
                    # weight = dynamic_cost(elevation_diff, elevation_data[j,i],elevation_data[j,i-1])
                    self.graph.add_edge(prevCoordinate,currCoordinate)

                prevCoordinate = currCoordinate

            prevRow = currentRow

    """
    Function takes in the difference in elevation of the current pixel and the next pixel
    Requires:
        - elevation_diff: difference in elevation between the current pixel and next pixel
        - current_pixel: the pixel array that has height stored in it
        - neighbor_pixel: the pixel array next to the current_pixel that holds the height
    """
    def dynamic_cost(elevation_diff, current_pixel, neighbor_pixel):
        cost = elevation_diff

        #in progress
        #if 

        return cost

    """
    Function finds the best possible path using the graph, starting location, target location, and weight
    Requires:
        - self.graph: location wehre the graph is stored at
        - currentLocation: starting location of the user
        - target: destination of the path
        - weight: the calculated weight given in each of the nodes
        - transform: variable that helsp in calculating the coordinates
    """
    def findBestPath(self, currentLocation, target, weight, transform):
        # TODO: Attempt to find shortest path without water, then find longest path with water
        # path = nx.shortest_path(self.graph, currentLocation, target, weight = 'weight')
        # geo_path = [transform *(x,y) for x,y in path]
        return path

    def updateMap(self, newElevationMap, newHeatMap):
        self.elevationImage = Image.open(newElevationMap)
        self.heatMap = Image.open(newHeatMap)

    