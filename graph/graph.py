from __future__ import annotations
"""
In this file everything concerning the creation of a graph is contained.


"""

from typing import Dict, Tuple, List, Union, cast, NewType

import geopy.distance as geodist


# Define a position
Position = NewType ("Position", Tuple[int, int])


# Define a position in geographical coordinates
Geoposition = NewType ("Geoposition", Tuple[float,float])






def _euclidean (pos1 : Position, pos2 : Position) -> int:
	"""
	This method returns the euclidean distance between two positions.

	:param pos1: First position.
	:param pos2: Second position.
	:return: The euclidean distance.

	"""
	return int(((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5)









class Node (object):
	"""
	An instance of this class represents a node of the Graph.

	"""
	def __init__ (self, id : int, pos : Tuple[int,int], active : bool = False) -> None:
		"""
		Initialize.
		
		:attr id: The unique id.
		:attr pos: The position of the node in coordinates (i.e. x and y).
		:attr active: If TRUE the node represents a real element of interest (e.g. building,
						factory, hub, etc.)

		"""
		self.id = id
		self.pos = cast(Position, pos)
		self.active = active







class Geonode (object):
	"""
	An instance of this class represents a node of the Graph
	if its position is defined by geographical coordinates.

	"""
	def __init__ (self, id : int, geopos : Tuple[float,float], active : bool = False) -> None:
		"""
		Initialize.
		
		:attr id: The unique id.
		:attr pos: The position of the node in geographical coordinates (i.e. lat and lon)
		:attr active: If TRUE the node represents a real element of interest (e.g. building,
						factory, hub, etc.)

		"""
		self.id = id
		self.pos = cast (Geoposition, geopos)
		self.active = active








class Edge (object):
	"""


	"""
	def __init__ (self,
				origin : Union[Node, Geonode],
				destination : Union[Node, Geonode],
				length : Optional[int] = None,
				oneway : bool = False
				) -> None:
		"""
		Initialize.



		"""
		self.nodes : Union[Tuple[Node, Node],Tuple[Geonode, Geonode]] = (origin, destination)
		self.length = length or int(geodist.geodesic(origin.pos, destination.pos).m) if type(origin) is Geonode else _euclideant(origin.pos, destination.pos)
		self.oneway = oneway