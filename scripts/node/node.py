"""
    A class that contains data for a node
"""
class Node:

    elevation = 0
    latitude = 0
    longitude = 0
    # frp = 0

    def __init__(self, elevation, latitude, longitude):
        self.elevation = elevation
        self.latitude = latitude
        self.longitude = longitude
        #self.frp = frp