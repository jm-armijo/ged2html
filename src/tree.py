class Tree():
	'''
	Creates a new Tree object.
	At least 1 valid Person object must be passed in the 'people' argument
	'''
	def __init__(self, people):
		self.nodes = dict()
		self.people = people

		level = 0
		starting_person = self._getStartingPerson()
		self._addPerson(level, starting_person)

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

	def _appendOnLevel(self, level, node):
		if level not in self.nodes:
			self.nodes[level] = list()
		self.nodes[level].append(node)

	def _addPerson(self, level, person):
		if len(person.unions) == 0:
			self._appendOnLevel(level, person)
		else:
			self._addUnions(level, person.unions)

	def _addUnions(self, level, unions):
		for union in unions:
			self._appendOnLevel(level, union)
			self._addChildren(level+1, union.children)

	def _addChildren(self, level, children):
		for child in children:
			self._addPerson(level, child)

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
