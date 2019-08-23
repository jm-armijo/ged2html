from collections import deque
from src.person import Person
from src.unique_queue import unique_queue

class Tree():
	'''
	Creates a new Tree object.
	At least 1 valid Person object must be passed in the 'people' argument
	'''
	def __init__(self, people):
		self.nodes = dict()
		self.opened = list()
		self.people = people

		level = 0
		starting_person = self._getStartingPerson()

		self._extendNodesAndAdd(0, [starting_person])

	def toHTML(self):
		html_tree = ''
		for level in reversed(self._getLevels()):
			html_tree += self._levelToHTML(level)

		return html_tree


	def _levelToHTML(self, level):
		return (
			'<div class="level">\n'
			'{}\n'
			'</div>\n'
		).format(self._nodesToHTML(self.nodes[level]))

	def _nodesToHTML(self, nodes):
		html_nodes = ''
		for node in nodes:
			html_nodes += self._nodeToHTML(node)
		return html_nodes

	def _nodeToHTML(self, node):
		return (
			'<div class="node">\n'
			'{}\n'
			'</div>'
		).format(node.toHTML())

	# Example tree
	#            [ A & B ]
	#              /   \
	#        [C & D]  [E & G]
	#            \
	#            F

	def _addNodes(self, level, nodes):
		for node in nodes:
			self._addNode(level, node)

	def _openNode(self, node):
		self.opened.append(node.id)

	def _addNode(self, level, node):
		if node.id in self.opened:
			return

		self._openNode(node)
		self._addToTree(level, node)
		self._extendNodesAndAdd(level+1, node.getChildren())
		self._extendNodesAndAdd(level-1, node.getParents())

	def _extendNodesAndAdd(self, level, nodes):
		extended = self._extendNodes(nodes)
		self._addNodes(level, extended)

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
	def _getStartingPerson(self):
		person = None
		people_ids = list(self.people.keys())

		if len(people_ids) > 0:
			people_ids.sort()
			person_id = people_ids[0]
			person = self.people[person_id]

		return person

	def _addToTree(self, level, node):
		if level not in self.nodes:
			self.nodes[level] = list()
		self.nodes[level].append(node)

	def _getLevels(self):
		levels = list(self.nodes.keys())
		levels.sort()
		return levels

	def __str__(self):
		to_str = ""

		for level in self._getLevels():
			for union in self.nodes[level]:
				to_str += str(union)
			to_str += '\n'

		return to_str
