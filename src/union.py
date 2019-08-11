class Union():
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

	def __str__(self):
		to_str = "{} & {} ({}, {}) --> ".format(self.spouse1, self.spouse2, self.place, self.date)
		for child in self.children:
			to_str += "{} ".format(child)
		return to_str
