import sys 
import os

# Append path for node
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'node')))

import networkx as nx
from node import Node
import numpy as np
import rasterio
import pandas as pd

class TerrainGraph:

    graph = 0
    width = 0
    height = 0
    latitudeLongitudeMapping = {}

    """
    Gets the desitination or target using the source of the fire and current location of user
    Requires:
        - file: input a csv file to extract the information of the wildfires and the source
    Outputs:
        - target: destination of the desired route and used to calculate path
    """
    def get_destination(file):
        csv_file = pd.read_csv(file)

        latitudes = csv_file['LATITUDE,N,32,10']
        longitudes = csv_file['LONGITUDE,N,32,10']
        power = csv_file['FRP,N,32,10']

        source_FRP = max(power)
        index = np.argmax(power)
        target = (longitudes[index],latitudes[index])

        return target

    """
    Unpacks a csv file from the user and outputs the altitude, latitude and longitude
    Requires:
        - file: input a csv file to extract the information of the wildfires and the source
    Outputs:
        - longitudes: outputs the longitude array containing the values of the longitudes
        - latitudes: outputs the latitude array containing the values of the latitudes
        - altitudes: outputs the altitude array containing the altitudes values
    """
    def unpack_csv(file):
        csv_file = pd.read_csv(file)

        latitudes = csv_file['LATITUDE,N,32,10']
        longitudes = csv_file['LONGITUDE,N,32,10']
        altitudes = csv_file['Altitude']                #change its name

        return longitudes,latitudes,altitudes

    """
    Initializes the graph for pathfinding
    Requires:
        - nodeMapping: a 2d array containing nodes (contains values of height, longitude and latitude)
        - width: width of nodeMapping window
        - height: height of nodeMapping window
    """
    def __init__(self, nodeMapping, width, height):
        self.graph = nx.Graph()
        self.width = width
        self.height = height

        # Rows along the image
        prevRow = []
        currentRow = []

        for j in range(height):
            prevCoordinate = ()
            for i in range(width):
                currCoordinate = (i, j)
                if nodeMapping == None:
                    currentRow.append(None)
                    continue

                self.graph.add_node(currCoordinate)
                self.graph.nodes[currCoordinate]['elevation'] = nodeMapping[j][i].elevation
                self.graph.nodes[currCoordinate]['longitude'] = nodeMapping[j][i].longitude
                self.graph.nodes[currCoordinate]['latitude'] = nodeMapping[j][i].latitude

                currentRow.append(currCoordinate)
                self.latitudeLongitudeMapping.update({(nodeMapping[j][i].latitude, nodeMapping[j][i].longitude) : (i, j)})

                if j > 0 and prevRow[i] != None: # Connect node from above
                    elevation_diff = abs(nodeMapping[j][i].elevation - nodeMapping[j-1][i].elevation)
                    self.graph.add_edge((i, j-1),currCoordinate, weight=elevation_diff)

                if i > 0 and currentRow[len(currentRow) - 1] != None: # Connect node from left side
                    elevation_diff = abs(nodeMapping[j][i].elevation - nodeMapping[j][i-1].elevation)
                    self.graph.add_edge(prevCoordinate, currCoordinate, weight=elevation_diff)

                prevCoordinate = currCoordinate

            prevRow = currentRow
            currentRow = []

    """
    Function finds the best possible path if given the start point of the search and the end
    Requires:
        - source: the source/starting point of the search (latitude, longitude)
        - dest: the end point of our search (latitude, longitude)
    Returns:
        - A list of longitudes that map the path from point A to point B
    """
    def findBestPath(self, source, dest):
        sourceCoordinate = self.convertLatitudeLongitude(source)
        destCoordinate = self.convertLatitudeLongitude(dest)
        shortestPath = nx.shortest_path(self.graph, sourceCoordinate, destCoordinate, weight='weight')

        print(shortestPath)

        coordinateList = []
        for point in shortestPath:
            coordinateList.append((self.graph.nodes[point]['latitude'], self.graph.nodes[point]['longitude']))
            
        return coordinateList

    """
    Gives width,height coordinates of a node given the latitude and longitude
    Requires:
        - positioning: a tuple in the form (latitude, longitude)
    Returns:
        - The equivalent tuple at the given latitude and longitude
    """
    def convertLatitudeLongitude(self, positioning): 
        return self.latitudeLongitudeMapping[positioning]

    # TODO: Implement a function to update individual nodes to avoid having to recall the constructor and rebuild
    #       the entire graph
    """
    Update attributes of the map instead of reconstructing it
    Requires:
        - positioning: the position of the node as (latitude, longitude)
        - attributeKey: the name of the attribute
        - arrributeValue: the new value of the attribute
    Returns:
        - Nothing
    """
    def updateNode(self, positioning, attributeKey, attributeValue):
        print('hi')
