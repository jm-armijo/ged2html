from collections import deque
from src.person import Person

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

	# Example tree
	#            [ A & B ]
	#              /   \
	#        [C & D]  [E & G]
	#            \
	#            F

	def _addNodes(self, level, nodes):
		for node in nodes:
			self._addNode(level, node)

	def _addNode(self, level, node):
		if node.id in self.opened:
			return

		self.opened.append(node.id)
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

	# TODO : make this return for person and unions
	def _extendNode(self, node):
		if isinstance(node, Person):
			return [node]

		union = node
		count = 0
		opened = list()
		to_open = deque([union])

		while (len(to_open) > 0):
			union = to_open.popleft()
			opened.append(union)

			unions = union.getUnions()

			for union in unions:
				if union not in opened:
					to_open.append(union)

		return opened

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
