
# Imports from Python 3 libraries
# Note: osmnx, geopandas, networkx must be installed via Conda
import osmnx as ox  # conda install -c conda-forge osmnx
import geopandas as gpd
import networkx as nx
import shapely.geometry as shly
import pandas as pd
import matplotlib.pyplot as plt
import collections
import random



# A wrapper for the nodes is created to make them easier to handle for future scopes
# :param geopd_obj: The real Geopandas object is kept and saved here
# :param osmid: <int> The osmid, i.e. unique id for the node
# :param x: <float> The x coordinate on the plane
# :param y: <float> The y coordinate on the plane
# :param lat: <float> The latitude
# :param lon: <float> The longitude
# :param geometry: <Shapely.geometry> The representation in the map
Node = collections.namedtuple ("Node", "geopd_obj osmid x y lat lon geometry")





# A wrapper for the edges is created to make them easier to handle for future scopes
# :param geopd_obj: The real Geopandas object is kept and saved here
# :param osmid: <int> The osmid unique id
# :param name: <str> The name of the street
# :param highway: <str> The type of street
# :param oneway: <bool> True if the street is oneway, false otherwise
# :param length: <float> The length of the street in metres [m]
# :param geometry: <Shapely.geometry> The geometric representation of the street
# :param maxspeed: <optional><int> The max speed allowed on that street (when known)
# :param lanes: <int> The number of lanes on the street
# :param u: <int> The osmid of the starting node
# :param v: <int> The osmid of the ending node
Edge = collections.namedtuple ("Edge", "geopd_obj osmid name highway oneway length geometry maxspeed lanes u v")





class MapScraper (object):
    """
    An instance of this class represents the map scraper.
    It is able to send http requests to OpenMaps to download streets, buildings, shops,
    crosses, companies, etc.
    It is also enriched with a set of tools to speed up the development of simulations
    and algorithm of the extracted graph of roads.
    Objects, types and classes are essentially coming from Geopandas and Pandas, although
    a further interface more familiar for industrial practictioners has been developed.

    """
    def __init__ (self, village, province, country, roads_type='drive'):
        """
        Initialize.

        :param village: <str> The village to download from OpenMaps
        :param province: <str> The province the villange belongs to
        :param country: <str> The country
        :param roads_type: <str> The type of roads to download. Possibilities
                            are drive, bike, and walk.

        :attr place_name: <str> The place downloaded from OpenMaps
        :attr nodes: <dict> The list of nodes
        :attr edges: <dict> The list of edges
        :attr graph: <networkx.classes.multidigraph.MultiDiGraph> The full graph object

        """
        self.place_name = ", ".join((village, province, country))
        print (f"Scraping of {self.place_name}...", end="")
        g = ox.project_graph(ox.graph_from_place (self.place_name, network_type=roads_type))
        self.nodes_gpd, self.edges_gpd = ox.graph_to_gdfs (g, nodes=True, edges=True)
        self.nodes = {i : Node(n, n.osmid, n.x, n.y, n.lat, n.lon, n.geometry) for i, n in self.nodes_gpd.iterrows()}
        self.edges = {i : Edge(e, e.osmid, e.name, e.highway, e.oneway, e.length, e.geometry, e.maxspeed, e.lanes, e.u, e.v)
                           for i, e in self.edges_gpd.iterrows()}
        self.graph = g
        print ("done")


    def plot_graph (self):
        """
        This method provides a representation of the map downloaded.
        Further packages by Geopython might be used to improve the representation,
        but, for the moment I kept it simple.

        :return: None
        """
        ox.plot_graph(self.graph)


    @property
    def stats (self):
        """
        This property returns some default statistics concerning the
        scraded graph.
        :return: <panda.Series> Default statistics
        """
        g, e = self.graph, self.edges_gpd
        area = e.unary_union.convex_hull.area
        stats = ox.basic_stats(g, area=area)
        extended_stats = ox.extended_stats(g, ecc=True, bc=True, cc=True)
        for key, value in extended_stats.items():
            stats[key] = value
        return pd.Series(stats)


    def random_nodes (self, n=2):
        """
        This method return a set of nodes randomly selected from the graph.
        :param n: The number of nodes to return
        :return: Random nodes
        """
        nodes_gpd, nodes = self.nodes_gpd, self.nodes
        return tuple(sc.nodes[int(dict(nodes_gpd.sample())["osmid"])] for _ in range(n))


    def random_gpd_nodes (self, n=2):
        """
        This method return a set of nodes randomly selected from the graph, keeping
        the GeoPython format of Points.
        :param n: The number of nodes to return
        :return: Random GeoPython nodes
        """
        nodes_gpd = self.nodes_gpd
        return tuple(nodes_gpd.sample() for _ in range(n))


    def get_path (self, origin, target, algorithm='dijkstra', verbose=True):
        """
        This pethod returns the shortest path between two nodes.
        The algorithms used to calculate the shortest path are the following:
            - Dijkstra (default)
            - Bellman-Ford
            - A* or A star
            - Floyd-Warshall
        The A* uses as heuristic the euclidean distance as the crow flies between the current
        node and the destination.
        The usage of the Floyd-Warshall is suggested only as double-check, since it requires
        a very long computational time, because it is of order O^3.

        :param origin: <tuple> Geographical coordinates for the node of origin, e.g. (lat, lon)
        :param target: <tuple> Geographical coordinates for the destination node, e.g. (lat, lon)
        :param algorithm: <str> The algorithm used to calculate the shortest path (default: djikstra)
        :param verbose: <bool> If True more details on the provided path are returned
        :return: <tuple> The nodes on the path between the origin and the destination and its length
        """
        g, n = self.graph, self.nodes_gpd
        orig_node = ox.get_nearest_node(g, origin, method='haversine')
        target_node = ox.get_nearest_node(g, target, method='haversine')

        if orig_node == target_node:
            raise ValueError ('The origin and the target must be different')

        if verbose:
            print ("\n An approximation has been made and the origin and target considered will be the following: ")
            print (gpd.GeoDataFrame([n.loc[orig_node], n.loc[target_node]], geometry='geometry', crs=n.crs), end="\n\n")

        route = None
        if algorithm == 'dijkstra':
            route = nx.shortest_path(G=g,source=orig_node,target=target_node,weight='length',method=algorithm)
        elif algorithm == 'bellman-ford':
            route = nx.shortest_path(G=g, source=orig_node, target=target_node, weight='length', method=algorithm)
        elif algorithm == 'astar':
            route = nx.astar_path (G=g,source=orig_node,target=target_node,weight='length',heuristic=None)
        elif algorithm == 'floyd-warshall':
            route = nx.floyd_warshall_numpy(G=g, nodelist=None, weight='length')
        else:
            raise NameError ('The algorithm required has not been found.')

        dist = sum(g[route[j]][route[j + 1]][0]['length'] for j in range(len(route) - 1))

        if verbose:
            print(f"The nodes to visit are the following: \n {route} \n")
            print(f"The total length of the path is: {dist}")

        return route, dist


    def plot_path (self, route):
        """
        This method plot the path found.

        :param route: The list of visited nodes
        :return: None
        """
        ox.plot_graph_route(self.graph, route)
