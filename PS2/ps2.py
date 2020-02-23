# 6.0002 Problem Set 5
# Graph optimization
# Name:
# Collaborators:
# Time:

#
# Finding shortest paths through MIT buildings
#
import unittest
from graph import Digraph, Node, WeightedEdge

#
# Problem 2: Building up the Campus Map
#
# Problem 2a: Designing your graph
#
# What do the graph's nodes represent in this problem? What
# do the graph's edges represent? Where are the distances
# represented?
#
# Answer: Nodes are the various buildings on the MIT campus. The graphs edges are represented by which buildings are next to each other in space. 
#Followed by the total distance between and then the outside distance. 
#


# Problem 2b: Implementing load_map
def load_map(map_filename):
	"""
	Parses the map file and constructs a directed graph

	Parameters:
		map_filename : name of the map file

	Assumes:
		Each entry in the map file consists of the following four positive
		integers, separated by a blank space:
			From To TotalDistance DistanceOutdoors
		e.g.
			32 76 54 23
		This entry would become an edge from 32 to 76.

	Returns:
		a Digraph representing the map
	"""

	print("Loading map from file...")
	with open(map_filename) as f :
		edge_list = [line.rstrip('\n') for line in f]
	edge_list2 = []
	for edge in edge_list:
		split_edge = edge.split()
		edge_list2.append(split_edge)
	digraph = Digraph()
	nodes = []	
	for edge in edge_list2:
		if Node(str(edge[0])) not in nodes:
			nodes.append(Node(str(edge[0])))
		else:
			continue 	
	for n in nodes:
		digraph.add_node(n)
	for edge in edge_list2:
		node1 = Node(str(edge[0]))
		node2 = Node(str(edge[1]))
		Weighted_Edge = WeightedEdge(node1, node2, edge[2], edge[3])
		digraph.add_edge(Weighted_Edge)
	return digraph	

# Problem 3b: Implement get_best_path
def get_best_path(digraph, start, end, path1, path2, path, max_total_dist, max_dist_outdoors, best_dist,
				  best_path):
	"""
	Finds the shortest path between buildings subject to constraints.

	Parameters:
		digraph: Digraph instance
			The graph on which to carry out the search
		start: string
			Building number at which to start
		end: string
			Building number at which to end
		path: list composed of [[list of strings], int, int]
			Represents the current path of nodes being traversed. Contains
			a list of node names, total distance traveled, and total
			distance outdoors.
		max_dist_outdoors: int
			Maximum distance spent outdoors on a path
		best_dist: int
			The smallest distance between the original start and end node
			for the initial problem that you are trying to solve
		best_path: list of strings
			The shortest path found so far between the original start
			and end node.

	Returns:
		A tuple with the shortest-path from start to end, represented by
		a list of building numbers (in strings), [n_1, n_2, ..., n_k],
		where there exists an edge from n_i to n_(i+1) in digraph,
		for all 1 <= i < k and the distance of that path.

		If there exists no path that satisfies max_total_dist and
		max_dist_outdoors constraints, then return None.
	"""
	# TODO	
	from itertools import islice 
	path = [path[0] + [start], path[1] + path1 , path[2] + path2] # adds values to the path to keep track of wheere th search is. Key to the recursion.
	if digraph.has_node(start) == False or digraph.has_node(end) == False:
		raise ValueError("start or end are not nodes")
	elif start == end and path[1] <= max_total_dist and path[2] <= max_dist_outdoors: # allows an exit out of the recursion through returning a value 
		if best_dist == 0:
			return path 
		elif path[1] <= best_dist:
			return path 
	else:
		edges = digraph.get_edges_for_node(start)
		dest_list = list(islice(edges, 0, None, 3))
		t_d_list = list(islice(edges, 1, None, 3))
		o_d_list = list(islice(edges, 2, None, 3))
		for node, t_d, o_d in zip(dest_list, t_d_list, o_d_list): #this givess access to the destination node and the weights of the edge
			if node not in path[0]:
				if best_path == None and path[1] <= max_total_dist and path[2] <= max_dist_outdoors or path[1] < best_dist and path[1] <= max_total_dist and path[2] <= max_dist_outdoors:
					newpath = get_best_path(digraph, node, end, int(t_d), int(o_d), path, max_total_dist, max_dist_outdoors, best_dist,
				  best_path) # this recursivley looks down the children of start node 
					if newpath != None: # if start == end does not return anything then no path has been found and can back up recursion 
							best_path = newpath
							best_dist = newpath[1]
		return(best_path)

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
	"""
	Finds the shortest path from start to end using a directed depth-first
	search. The total distance traveled on the path must not
	exceed max_total_dist, and the distance spent outdoors on this path must
	not exceed max_dist_outdoors.

	Parameters:
		digraph: Digraph instance
			The graph on which to carry out the search
		start: string
			Building number at which to start
		end: string
			Building number at which to end
		max_total_dist: int
			Maximum total distance on a path
		max_dist_outdoors: int
			Maximum distance spent outdoors on a path

	Returns:
		The shortest-path from start to end, represented by
		a list of building numbers (in strings), [n_1, n_2, ..., n_k],
		where there exists an edge from n_i to n_(i+1) in digraph,
		for all 1 <= i < k

		If there exists no path that satisfies max_total_dist and
		max_dist_outdoors constraints, then raises a ValueError.
	"""
	shortest_path = get_best_path(digraph, Node(start), Node(end), 0, 0, [[], 0, 0], max_total_dist, max_dist_outdoors, best_dist = 0, best_path = None)
	shortest_path_str_list = []
	if shortest_path == None:
		raise ValueError("No path found")
	for x in shortest_path[0]:
		y = str(x)
		shortest_path_str_list.append(y)
	return shortest_path_str_list	
		

	

# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
	LARGE_DIST = 99999

	def setUp(self):
		self.graph = load_map("mit_map.txt")

#	def test_load_map_basic(self):
#		self.assertTrue(isinstance(self.graph, Digraph))
#		self.assertEqual(len(self.graph.nodes), 37)
#		all_edges = []
#		for _, edges in self.graph.edges.items():
#		    all_edges += edges	# edges must be dict of node -> list of edges
#		    all_edges = set(all_edges)
#		    self.assertEqual(len(all_edges), 129)

	def _print_path_description(self, start, end, total_dist, outdoor_dist):
		constraint = ""
		if outdoor_dist != Ps2Test.LARGE_DIST:
			constraint = "without walking more than {}m outdoors".format(
				outdoor_dist)
		if total_dist != Ps2Test.LARGE_DIST:
			if constraint:
				constraint += ' or {}m total'.format(total_dist)
			else:
				constraint = "without walking more than {}m total".format(
					total_dist)

		print("------------------------")
		print("Shortest path from Building {} to {} {}".format(
			start, end, constraint))

	def _test_path(self,
				   expectedPath,
				   total_dist=LARGE_DIST,
				   outdoor_dist=LARGE_DIST):
		start, end = expectedPath[0], expectedPath[-1]
		self._print_path_description(start, end, total_dist, outdoor_dist)
		dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
		print("Expected: ", expectedPath)
		print("DFS: ", dfsPath)
		self.assertEqual(expectedPath, dfsPath)

	def _test_impossible_path(self,
							  start,
							  end,
							  total_dist=LARGE_DIST,
							  outdoor_dist=LARGE_DIST):
		self._print_path_description(start, end, total_dist, outdoor_dist)
		with self.assertRaises(ValueError):
			directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

	def test_path_one_step(self):
		self._test_path(expectedPath=['32', '56'])

	def test_path_no_outdoors(self):
		self._test_path(
			expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

	def test_path_multi_step(self):
		self._test_path(expectedPath=['2', '3', '7', '9'])

	def test_path_multi_step_no_outdoors(self):
		self._test_path(
			expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

	def test_path_multi_step2(self):
		self._test_path(expectedPath=['1', '4', '12', '32'])

	def test_path_multi_step_no_outdoors2(self):
		self._test_path(
			expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
			outdoor_dist=0)

	def test_impossible_path1(self):
		self._test_impossible_path('8', '50', outdoor_dist=0)

	def test_impossible_path2(self):
		self._test_impossible_path('10', '32', total_dist=100)


if __name__ == "__main__":
	unittest.main()
