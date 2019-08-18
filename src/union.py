from src.node import Node

class Union(Node):
	def __init__(self, id):
		self.id = id
		self.spouse1 = None
		self.spouse2 = None
		self.children = list()
		self.date = None
		self.place = None

	def setSpouse1(self, spouse):
		spouse.addUnion(self)
		self.spouse1 = spouse

	def setSpouse2(self, spouse):
		spouse.addUnion(self)
		self.spouse2 = spouse

	def addChild(self, child):
		child.setParents(self)
		self.children.append(child)

	def setDate(self, date):
		self.date = date

	def setPlace(self, place):
		self.place = place

	def getChildren(self):
		return self.children

	def getParents(self):
		parents = list()
		if self.spouse1 is not None:
			parents += self.spouse1.getParents()
		if self.spouse2 is not None:
			parents += self.spouse2.getParents()

		return parents

	def getUnions(self):
		parents = list()
		if self.spouse1 is not None:
			parents += self.spouse1.getUnions()
		if self.spouse2 is not None:
			parents += self.spouse2.getUnions()

		return parents
	def __str__(self):
		to_str = "{{ {} & {} }}".format(self.spouse1, self.spouse2)
		return to_str
