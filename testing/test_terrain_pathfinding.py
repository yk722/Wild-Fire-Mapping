import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'terrain_pathfinding')))

import networkx as nx
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import numpy as np
from terrain_pathfinding import TerrainGraph
import unittest

class TestTerrainGraph(unittest.TestCase):

    def test1x1(self):
        imagePath = os.path.join(os.getcwd(), 'green-1x1.png')
        terrainG = TerrainGraph(imagePath)
        self.assertTrue(terrainG.graph.has_node((0,0)))
    
    def test3x1(self):
        imagePath = os.path.join(os.getcwd(), 'rgb-3x1.png')
        terrainG = TerrainGraph(imagePath)
        self.assertTrue(terrainG.graph.has_node((0,0)))
        self.assertTrue(terrainG.graph.has_node((1,0)))
        self.assertTrue(terrainG.graph.has_node((2,0)))
        self.assertTrue(terrainG.graph.has_edge((1,0), (0,0)))
        self.assertTrue(terrainG.graph.has_edge((2,0), (1,0)))

    def test2x5(self):
        imagePath = os.path.join(os.getcwd(), 'mix-2x5.png')
        terrainG = TerrainGraph(imagePath)
        self.assertTrue(terrainG.graph.has_node((0,0)))
        self.assertTrue(terrainG.graph.has_node((0,1)))
        self.assertTrue(terrainG.graph.has_node((0,2)))
        self.assertTrue(terrainG.graph.has_node((0,3)))
        self.assertTrue(terrainG.graph.has_node((0,4)))
        self.assertTrue(terrainG.graph.has_node((1,0)))
        self.assertTrue(terrainG.graph.has_node((1,1)))
        self.assertTrue(terrainG.graph.has_node((1,2)))
        self.assertTrue(terrainG.graph.has_node((1,3)))
        self.assertTrue(terrainG.graph.has_node((1,4)))

        self.assertTrue(terrainG.graph.has_edge((0,0), (1,0)))
        self.assertTrue(terrainG.graph.has_edge((0,1), (1,1)))
        self.assertTrue(terrainG.graph.has_edge((0,2), (1,2)))
        self.assertTrue(terrainG.graph.has_edge((0,3), (1,3)))
        self.assertTrue(terrainG.graph.has_edge((0,4), (1,4)))

        self.assertTrue(terrainG.graph.has_edge((0,0), (0,1)))
        self.assertTrue(terrainG.graph.has_edge((0,1), (0,2)))
        self.assertTrue(terrainG.graph.has_edge((0,2), (0,3)))
        self.assertTrue(terrainG.graph.has_edge((0,3), (0,4)))

        self.assertTrue(terrainG.graph.has_edge((1,0), (1,1)))
        self.assertTrue(terrainG.graph.has_edge((1,1), (1,2)))
        self.assertTrue(terrainG.graph.has_edge((1,2), (1,3)))
        self.assertTrue(terrainG.graph.has_edge((1,3), (1,4)))

    def testTIF(self):
        rasterPath = os.path.join(os.getcwd(), 'bc_xc100m_bcalb', 'bc_xc100m_bcalb_20070116.tif')
        terrainG = TerrainGraph(rasterPath)

        nx.draw(terrainG.graph, node_size=350, edge_color='gray')

        plt.title("test")
        plt.show()

if __name__ == '__main__':
    unittest.main()