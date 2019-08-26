from collections import deque
from src.edge import Edge
from src.html import HTMLGenerator
from src.person import Person
from src.tree_level import TreeLevel
from src.unique_queue import unique_queue

class Tree():
	'''
	Creates a new Tree object.
	At least 1 valid Person object must be passed in the 'people' argument
	'''
	def __init__(self, nodes, unions):
		self.levels = dict()
		self.opened = list()
		self.nodes = nodes

		level = 0
		starting_node = self._getStartingNode()
		self._extendNodeAndAdd(0, starting_node)
		self.edges = self._createEdges(unions)

	def toHTML(self):
		nodes = HTMLGenerator.listToHTML(self._getLevels())
		edges = HTMLGenerator.listToHTML(self.edges)
		edges_script = HTMLGenerator.getOnLoadScript(edges)

		return (
			'{}'
			'{}'
		).format(nodes, edges_script)

	def _createEdges(self, unions):
		edges = list()
		for union in unions:
			edges += self._createdEdgesFromNode(union)
		return edges

	def _createdEdgesFromNode(self, start):
		edges = list()
		if start not in self.opened:
			print("Element {} not processed. Check your ged file for inconsistent data.".format(start.id))
		else:
			edges = self._createEdgesToNodes(start, start.getChildren())
		return edges

	def _createEdgesToNodes(self, start, end_nodes):
		edges = list()
		for end in end_nodes:
			edges += self._createEdgeToNode(start, end)
		return edges

	def _createEdgeToNode(self, start, end):
		edges = list()
		if end not in self.opened:
			print("Element {} not processed. Check your ged file for inconsistent data.".format(end.id))
		else:
			edges.append(Edge(start.id, end.id))
		return edges

	def _extendNodesAndAdd(self, level, nodes):
		for node in nodes:
			self._extendNodeAndAdd(level, node)

	def _extendNodeAndAdd(self, level, node):
		extended = self._extendNode(node)
		self._addNodes(level, extended)

	def _addNodes(self, level, nodes):
		for node in nodes:
			self._addNode(level, node)

	def _addNode(self, level, node):
		if node in self.opened:
			return

		self._openNode(node)
		self._addToTree(level, node)
		self._extendNodesAndAdd(level+1, node.getChildren())
		self._extendNodesAndAdd(level-1, node.getParents())

	def _openNode(self, node):
		self.opened.append(node)

	def _extendNodes(self, nodes):
		extended = list()
		for node in nodes:
			extended += self._extendNode(node)
		return extended

	def _extendNode(self, node):
		if isinstance(node, Person):
			return self._extendPerson(node)
		else:
			return self._extendUnion(node)

	def _extendPerson(self, person):
		if person.isSingle():
			return [person]
		else:
			self._openNode(person)
			return self._extendNodes(person.getUnions())

	def _extendUnion(self, union):
		queue = unique_queue([union])

		while (not queue.isEmpty()):
			union = queue.pop()
			queue.pushList(union.getUnions())

		return queue.getAll()

	'''
	Gets a Person object to start building the tree.
	It can be any person, so the one with the lowest id is picked
	'''
	def _getStartingNode(self):
		node = None
		people_ids = list(self.nodes.keys())

		if len(people_ids) > 0:
			people_ids.sort()
			person_id = people_ids[0]
			node = self.nodes[person_id]

		return node

	def _addToTree(self, level, node):
		if level not in self.levels:
			self.levels[level] = TreeLevel()
		self.levels[level].append(node)

	def _getLevels(self):
		keys = sorted(self.levels.keys(), reverse=True)
		levels = []
		for key in keys:
			levels.append(self.levels[key])
		return levels
