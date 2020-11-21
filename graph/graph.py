"""
In this file everything concerning the creation of a graph is contained.


< NODES >
Each geographical position can be represented as a Node or a Geonode. The Node is 
characterised by planar coordinates, while the Geonode is characterised by 
geographical coordinates (i.e. latitude and longitude).
Each node can be marked as active if it represents a position of interest, such as
a company, a shop, or a monument.


< EDGES >
Each edge connect two different nodes (i.e. origin and destination), it has a length
(geographical or euclidean distance between the origin and the destination), and it
can be marked as one-way, i.e. it can be runned only going from the origin to the 
destination.


< GRAPH >
The graph object has a list of nodes and a list of edges connecting these nodes.
It also has a distance matrix where distances[i][j] means that node i is directly 
connected to node j (with i and j are the ids of the respective nodes).
Undirect connections are not reported. Finding them is task of the A* algorithm or
any other optimizer.


"""
import geopy.distance as geodist






class Node (object):
	"""
	An instance of this class represents a node of the Graph.

	"""
	def __init__ (self, id, pos, active=False):
		"""
		Initialize.
		
		:attr id: The unique id.
		:attr pos: The position of the node in coordinates (i.e. x and y).
		:attr active: If TRUE the node represents a real element of interest (e.g. building,
						factory, hub, etc.)

		"""
		self.id = id
		self.pos = pos
		self.active = active



	def __eq__ (self, other):
		"""
		Magic method that override the equality (==) operator.
		It returns True if the nodes are in the same position, False otherwise.
		It raise an Exception if the comparison is between a node and a Geonode.

		:param other: An other node:
		:return: True if the nodes are in the same position.

		"""
		if type(other) is Geonode:
			raise TypeError ("Comparison between a Node and a Geonode")

		return other.pos == self.pos



	def __ne__ (self, other):
		"""
		Magic method that override the inequality (!=) operator.
		It returns True if the nodes are NOT in the same position, False otherwise.
		It raise an Exception if the comparison is between a node and a Geonode.

		:param other: An other node:
		:return: True if the nodes are NOT in the same position.

		"""
		if type(other) is Geonode:
			raise TypeError ("Comparison between a Node and a Geonode")

		return other.pos != self.pos









class Geonode (object):
	"""
	An instance of this class represents a node of the Graph
	if its position is defined by geographical coordinates.

	"""
	def __init__ (self, id, geopos, active=False):
		"""
		Initialize.
		
		:attr id: The unique id.
		:attr pos: The position of the node in geographical coordinates (i.e. lat and lon)
		:attr active: If TRUE the node represents a real element of interest (e.g. building,
						factory, hub, etc.)

		"""
		self.id = id
		self.pos = geopos
		self.active = active




	def __eq__ (self, other):
		"""
		Magic method that override the equality (==) operator.
		It returns True if the nodes are in the same position, False otherwise.
		It raise an Exception if the comparison is between a node and a Node.

		:param other: An other node:
		:return: True if the nodes are in the same position.

		"""
		if type(other) is Node:
			raise TypeError ("Comparison between a Node and a Geonode")

		return other.pos == self.pos



	def __ne__ (self, other):
		"""
		Magic method that override the inequality (!=) operator.
		It returns True if the nodes are NOT in the same position, False otherwise.
		It raise an Exception if the comparison is between a node and a Geonode.

		:param other: An other node:
		:return: True if the nodes are NOT in the same position.

		"""
		if type(other) is Node:
			raise TypeError ("Comparison between a Node and a Geonode")

		return other.pos != self.pos









class Edge (object):
	"""
	An instance of this class represents and edge of the graph connecting two nodes.

	"""
	def __init__ (self, origin, destination, length=None, oneway=False):
		"""
		Initialize.

		:attr origin: The node of origin.
		:attr destination: The node of destination.
		:attr length: The length of the edge (if not provide is calculated as a 
						geographic distance in case of Geonodes and euclidean distance
						in case of Nodes.
		:attr oneway: If TRUE the edge in runnable only from the origin to the destination.)



		"""
		self.origin = origin
		self.destination = destination
		self.length = length or int(geodist.geodesic(origin.pos, destination.pos).m) if type(origin) is Geonode else self.__euclidean(origin.pos, destination.pos)
		self.oneway = oneway
		
		
	@staticmethod
	def __euclidean (pos1, pos2):
	"""
	This method returns the euclidean distance between two positions.

	:param pos1: First position.
	:param pos2: Second position.
	:return: The euclidean distance.

	"""
	return int(((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5)


	@property
	def nodes (self):
		"""
		It returns origin and destination in a different format.

		"""
		return self.origin, self.destination
	
	
	
class Graph (object):
	"""
	An instance of this class represents a graph.
	
	"""
	def __init__ (self, nodes, edges):
		"""
		Initialize.
		
		:attr nodes: The set of nodes.
		:attr edges: The set of edges.
		:attr distance: The matrix of distances between nodes.
		
		"""
		self.nodes = nodes
		self.edges = edges
		
		dists = {}
		for edge in edges:
			node1 = edge.origin.id; node2 = edge.destination.id
			if dists.get (node1):
				dists[node1][node2] = edge.length
			else:
				dists[node1] = {node2 : edge.length}
			
			if not edge.oneway:
				if dists.get (node2):
					dists[node2][node1] = edge.length
				else:
					dists[node2] = {node1 : edge.length}
					
		self.distances = dists
