
# Imports from Pyhton 3 libraries
# Note: osmnx, geopandas, networkx must be installed via Conda
import osmnx as ox  # conda install -c conda-forge osmnx
import geopandas as gpd
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import collections



# A wrapper for the nodes is created to make them easier to handle for future scopes
# :param geopd_obj: The real Geopandas object is kept and saved here
# :param id: The osmid, i.e. unique id for the node
# :param x: The x coordinate on the plane
# :param y: The y coordinate on the plane
# :param lat: The latitude
# :param lon: The longitude
# :param geometry: The representation in the map
Node = collections.namedtuple ("Node", "geopd_obj id x y lat lon geometry")





# A wrapper for the edges is created to make them easier to handle for future scopes
# :param geopd_obj: The real Geopandas object is kept and saved here
# :param id: <int> The osmid unique id
# :param name: <str> The name of the street
# :param highway: <str> The type of street
# ...
Edge = collections.namedtuple ("Edge", "geopd_obj id name highway oneway length geometry maxspeed lanes origin destination")





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
        :attr nodes: <tuple> The list of nodes
        :attr edges: <tuple> The list of edges
        :attr graph: <networkx.classes.multidigraph.MultiDiGraph> The full graph object
        """
        self.place_name = ", ".join((village, province, country))
        print (f"Scraping of {self.place_name}...", end="")
        g = ox.project_graph(ox.graph_from_place (self.place_name, network_type=roads_type))
        self.edges = ox.graph_to_gdfs (g, nodes=False, edges=True, fill_edge_geometry=True)
        self.nodes = ox.graph_to_gdfs (g, nodes=True, edges=False)
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






if __name__ == '__main__':
    sc = MapScraper("Bibbiano", "Reggio Emilia", "Italy")
    for i in sc.edges:
        print(i)

