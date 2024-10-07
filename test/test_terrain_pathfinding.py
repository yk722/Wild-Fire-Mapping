import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'terrain_pathfinding')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'node')))

import networkx as nx
import numpy as np
from node import Node
from terrain_pathfinding import TerrainGraph
import unittest

class TestTerrainGraph(unittest.TestCase):

    def test1x1Graph(self):
        width = 1
        height = 1
        nodeMapping = [[None] * height for _ in range(width)]
        node0 = Node(1,1,1)
        nodeMapping[0][0] = node0
        terrainGraph = TerrainGraph(nodeMapping, width, height)

        self.assertTrue(terrainGraph.graph.has_node((0,0)))
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['elevation'], 1)
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['latitude'], 1)
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['longitude'], 1)
        # self.assertEqual(terrainGraph.graph.nodes[(0,0)]['frp'], 1)

    def test2x1Graph(self):
        width = 2
        height = 1
        nodeMapping = [
            [Node(5,5,5), Node(1,1,1)]
        ]

        terrainGraph = TerrainGraph(nodeMapping, width, height)

        self.assertTrue(terrainGraph.graph.has_node((0,0)))
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['elevation'], 5)
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['latitude'], 5)
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['longitude'], 5)

        self.assertTrue(terrainGraph.graph.has_node((1,0)))
        self.assertEqual(terrainGraph.graph.nodes[(1,0)]['elevation'], 1)
        self.assertEqual(terrainGraph.graph.nodes[(1,0)]['latitude'], 1)
        self.assertEqual(terrainGraph.graph.nodes[(1,0)]['longitude'], 1)

        self.assertTrue(terrainGraph.graph.has_edge((0,0),(1,0)))

    def test1x2Graph(self):
        width = 1
        height = 2
        nodeMapping = [
            [Node(1,1,1)],
            [Node(5,5,5)]
        ]

        terrainGraph = TerrainGraph(nodeMapping, width, height)

        self.assertTrue(terrainGraph.graph.has_node((0,0)))
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['elevation'], 1)
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['latitude'], 1)
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['longitude'], 1)

        self.assertTrue(terrainGraph.graph.has_node((0,1)))
        self.assertEqual(terrainGraph.graph.nodes[(0,1)]['elevation'], 5)
        self.assertEqual(terrainGraph.graph.nodes[(0,1)]['latitude'], 5)
        self.assertEqual(terrainGraph.graph.nodes[(0,1)]['longitude'], 5)

        self.assertTrue(terrainGraph.graph.has_edge((0,0),(0,1)))

    def test3x3Graph(self):
        width = 3
        height = 3
        nodeMapping = [[None] * width for _ in range(height)]

        node00 = Node(1,0.1,0.1)
        node10 = Node(5,0.2,0.1)
        node20 = Node(3,0.3,0.1)
        node01 = Node(7,0.1,0.2)
        node11 = Node(1,0.2,0.2)
        node21 = Node(1,0.3,0.2)
        node02 = Node(3,0.1,0.3)
        node12 = Node(3,0.2,0.3)
        node22 = Node(2,0.3,0.3)

        nodeMapping[0][0] = node00
        nodeMapping[0][1] = node10
        nodeMapping[0][2] = node20
        nodeMapping[1][0] = node01
        nodeMapping[1][1] = node11
        nodeMapping[1][2] = node21
        nodeMapping[2][0] = node02
        nodeMapping[2][1] = node12
        nodeMapping[2][2] = node22

        terrainGraph = TerrainGraph(nodeMapping, width, height)

        print(terrainGraph.latitudeLongitudeMapping)

        self.assertTrue(terrainGraph.graph.has_node((0,0)))
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['elevation'], 1)
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['latitude'], 0.1)
        self.assertEqual(terrainGraph.graph.nodes[(0,0)]['longitude'], 0.1)
        # self.assertEqual(terrainGraph.graph.nodes[(0,0)]['frp'], 1)


        self.assertTrue(terrainGraph.graph.has_node((1,0)))
        self.assertEqual(terrainGraph.graph.nodes[(1,0)]['elevation'], 5)
        self.assertEqual(terrainGraph.graph.nodes[(1,0)]['latitude'], 0.2)
        self.assertEqual(terrainGraph.graph.nodes[(1,0)]['longitude'], 0.1)
        # self.assertEqual(terrainGraph.graph.nodes[(0,0)]['frp'], 1)

        self.assertTrue(terrainGraph.graph.has_node((2,0)))
        self.assertEqual(terrainGraph.graph.nodes[(2,0)]['elevation'], 3)
        self.assertEqual(terrainGraph.graph.nodes[(2,0)]['latitude'], 0.3)
        self.assertEqual(terrainGraph.graph.nodes[(2,0)]['longitude'], 0.1)
        # self.assertEqual(terrainGraph.graph.nodes[(0,0)]['frp'], 1)

        self.assertTrue(terrainGraph.graph.has_node((0,1)))
        self.assertEqual(terrainGraph.graph.nodes[(0,1)]['elevation'], 7)
        self.assertEqual(terrainGraph.graph.nodes[(0,1)]['latitude'], 0.1)
        self.assertEqual(terrainGraph.graph.nodes[(0,1)]['longitude'], 0.2)
        # self.assertEqual(terrainGraph.graph.nodes[(0,0)]['frp'], 1)

        self.assertTrue(terrainGraph.graph.has_node((1,1)))
        self.assertEqual(terrainGraph.graph.nodes[(1,1)]['elevation'], 1)
        self.assertEqual(terrainGraph.graph.nodes[(1,1)]['latitude'], 0.2)
        self.assertEqual(terrainGraph.graph.nodes[(1,1)]['longitude'], 0.2)
        # self.assertEqual(terrainGraph.graph.nodes[(0,0)]['frp'], 1)

        self.assertTrue(terrainGraph.graph.has_node((2,1)))
        self.assertEqual(terrainGraph.graph.nodes[(2,1)]['elevation'], 1)
        self.assertEqual(terrainGraph.graph.nodes[(2,1)]['latitude'], 0.3)
        self.assertEqual(terrainGraph.graph.nodes[(2,1)]['longitude'], 0.2)
        # self.assertEqual(terrainGraph.graph.nodes[(0,0)]['frp'], 1)

        self.assertTrue(terrainGraph.graph.has_node((0,2)))
        self.assertEqual(terrainGraph.graph.nodes[(0,2)]['elevation'], 3)
        self.assertEqual(terrainGraph.graph.nodes[(0,2)]['latitude'], 0.1)
        self.assertEqual(terrainGraph.graph.nodes[(0,2)]['longitude'], 0.3)
        # self.assertEqual(terrainGraph.graph.nodes[(0,0)]['frp'], 1)

        self.assertTrue(terrainGraph.graph.has_node((1,2)))
        self.assertEqual(terrainGraph.graph.nodes[(1,2)]['elevation'], 3)
        self.assertEqual(terrainGraph.graph.nodes[(1,2)]['latitude'], 0.2)
        self.assertEqual(terrainGraph.graph.nodes[(1,2)]['longitude'], 0.3)
        # self.assertEqual(terrainGraph.graph.nodes[(0,0)]['frp'], 1)

        self.assertTrue(terrainGraph.graph.has_node((2,2)))
        self.assertEqual(terrainGraph.graph.nodes[(2,2)]['elevation'], 2)
        self.assertEqual(terrainGraph.graph.nodes[(2,2)]['latitude'], 0.3)
        self.assertEqual(terrainGraph.graph.nodes[(2,2)]['longitude'], 0.3)
        # self.assertEqual(terrainGraph.graph.nodes[(0,0)]['frp'], 1)

        self.assertEqual(terrainGraph.convertLatitudeLongitude((0.1,0.2)), (0,1))

        self.assertTrue(terrainGraph.graph.has_edge((0,0),(1,0)))
        self.assertTrue(terrainGraph.graph.has_edge((1,0),(2,0)))
        
        self.assertTrue(terrainGraph.graph.has_edge((0,1),(1,1)))
        self.assertTrue(terrainGraph.graph.has_edge((1,1),(2,1)))

        self.assertTrue(terrainGraph.graph.has_edge((0,2),(1,2)))
        self.assertTrue(terrainGraph.graph.has_edge((1,2),(2,2)))

        self.assertTrue(terrainGraph.graph.has_edge((0,0),(0,1)))
        self.assertTrue(terrainGraph.graph.has_edge((1,0),(1,1)))
        self.assertTrue(terrainGraph.graph.has_edge((2,0),(2,1)))

        self.assertTrue(terrainGraph.graph.has_edge((0,1),(0,2)))
        self.assertTrue(terrainGraph.graph.has_edge((1,1),(1,2)))
        self.assertTrue(terrainGraph.graph.has_edge((2,1),(2,2)))

        self.assertFalse(terrainGraph.graph.has_edge((0,0),(1,1)))
        self.assertFalse(terrainGraph.graph.has_edge((0,1),(1,0)))

        self.assertEqual(terrainGraph.graph.get_edge_data((0,0), (1,0))['weight'], 4)
        self.assertEqual(terrainGraph.graph.get_edge_data((1,0), (2,0))['weight'], 2)
        
        self.assertEqual(terrainGraph.graph.get_edge_data((0,1), (1,1))['weight'], 6)
        self.assertEqual(terrainGraph.graph.get_edge_data((1,1), (2,1))['weight'], 0)

        self.assertEqual(terrainGraph.graph.get_edge_data((0,2), (1,2))['weight'], 0)
        self.assertEqual(terrainGraph.graph.get_edge_data((1,2), (2,2))['weight'], 1)

        self.assertEqual(terrainGraph.graph.get_edge_data((0,0), (0,1))['weight'], 6)
        self.assertEqual(terrainGraph.graph.get_edge_data((1,0), (1,1))['weight'], 4)
        self.assertEqual(terrainGraph.graph.get_edge_data((2,0), (2,1))['weight'], 2)

        self.assertEqual(terrainGraph.graph.get_edge_data((0,1), (0,2))['weight'], 4)
        self.assertEqual(terrainGraph.graph.get_edge_data((1,1), (1,2))['weight'], 2)
        self.assertEqual(terrainGraph.graph.get_edge_data((2,1), (2,2))['weight'], 1)

    # Verify manually
    def testPathFinding5x5(self):
        width = 5
        height = 5
        nodeMapping = [
            [Node(1, 0.1, 0.1), Node(75, 0.1, 0.2), Node(100, 0.1, 0.3), Node(1, 0.1, 0.4), Node(1, 0.1, 0.5)],
            [Node(100, 0.2, 0.1), Node(75, 0.2, 0.2), Node(100, 0.2, 0.3), Node(1, 0.2, 0.4), Node(1, 0.2, 0.5)],
            [Node(1, 0.3, 0.1), Node(1, 0.3, 0.2), Node(50, 0.3, 0.3), Node(50, 0.3, 0.4), Node(25, 0.3, 0.5)],
            [Node(1, 0.4, 0.1), Node(1, 0.4, 0.2), Node(50, 0.4, 0.3), Node(50, 0.4, 0.4), Node(25, 0.4, 0.5)],
            [Node(1, 0.5, 0.1), Node(75, 0.5, 0.2), Node(1, 0.5, 0.3), Node(1, 0.5, 0.4), Node(1, 0.5, 0.5)]
        ]

        terrainGraph = TerrainGraph(nodeMapping, width, height)

        latitudeLongitudeList = terrainGraph.findBestPath((0.5,0.5),(0.1,0.1))

if __name__ == '__main__':
    unittest.main()