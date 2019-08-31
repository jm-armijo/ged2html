from collections import deque
from src.edge import Edge
from src.html import HTMLGenerator
from src.person import Person
from src.tree_level import TreeLevel
from src.unique_queue import unique_queue

class Tree():

# public:

	'''
	Creates a new Tree object.
	At least 1 valid Person object must be passed in the 'people' argument
	'''
	def __init__(self, people, unions):
		self.levels = dict()
		self.opened = list()

		self.nodes = self._ceate_nodes(people)
		self.edges = self._create_edges(unions)

	def to_html(self):
		nodes_html = HTMLGenerator.list_to_html(self.nodes)
		edges_html = HTMLGenerator.list_to_html(self.edges)
		edges_script = HTMLGenerator.get_on_load_script(edges_html)

		return (
			'{}'
			'{}'
		).format(nodes_html, edges_script)

# private:

	def _ceate_nodes(self, people):
		level = 0
		starting_node = self._get_starting_node(people)
		self._extend_node_and_add(0, starting_node)
		return self._levels_to_nodes()

	def _extend_nodes_and_add(self, level, nodes):
		for node in nodes:
			self._extend_node_and_add(level, node)

	def _extend_node_and_add(self, level, node):
		extended = self._extend_node(node)
		self._add_nodes(level, extended)

	def _add_nodes(self, level, nodes):
		for node in nodes:
			self._add_node(level, node)

	def _add_node(self, level, node):
		if node in self.opened:
			return

		self._open_node(node)
		self._add_to_tree(level, node)
		self._extend_nodes_and_add(level+1, node.get_children())
		self._extend_nodes_and_add(level-1, node.get_parents())

	def _open_node(self, node):
		self.opened.append(node)

	def _extend_nodes(self, nodes):
		extended = list()
		for node in nodes:
			extended += self._extend_node(node)
		return extended

	def _extend_node(self, node):
		if isinstance(node, Person):
			return self._extend_person(node)
		else:
			return self._extend_union(node)

	def _extend_person(self, person):
		if person.is_single():
			return [person]
		else:
			self._open_node(person)
			return self._extend_nodes(person.get_unions())

	def _extend_union(self, union):
		queue = unique_queue([union])

		while (not queue.is_empty()):
			union = queue.pop()
			queue.push_list(union.get_unions())

		return queue.get_all()

	def _create_edges(self, unions):
		edges = list()
		for union in unions:
			edges += self._create_edges_from_node(union)
		return edges

	def _create_edges_from_node(self, start):
		edges = list()
		if start not in self.opened:
			print("Element {} not processed. Check your ged file for inconsistent data.".format(start.id))
		else:
			edges = self._create_edges_to_nodes(start, start.get_children())
		return edges

	def _create_edges_to_nodes(self, start, end_nodes):
		edges = list()
		for end in end_nodes:
			edges += self._create_edge_to_node(start, end)
		return edges

	def _create_edge_to_node(self, start, end):
		edges = list()
		if end not in self.opened:
			print("Element {} not processed. Check your ged file for inconsistent data.".format(end.id))
		else:
			edges.append(Edge(start.id, end.id))
		return edges

	'''
	Gets a Person object to start building the tree.
	It can be any person, so the one with the lowest id is picked
	'''
	def _get_starting_node(self, people):
		node = None
		people_ids = list(people.keys())

		if len(people_ids) > 0:
			people_ids.sort()
			person_id = people_ids[0]
			node = people[person_id]

		return node

	def _add_to_tree(self, level, node):
		if level not in self.levels:
			self.levels[level] = TreeLevel()
		self.levels[level].append(node)

	def _levels_to_nodes(self):
		keys = sorted(self.levels.keys(), reverse=True)
		nodes = []
		for key in keys:
			nodes.append(self.levels[key])
		return nodes
