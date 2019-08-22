from src.node import Node
from src.null_person import NullPerson

class Union(Node):
	def __init__(self, id):
		self.id = id
		self.spouse1 = NullPerson()
		self.spouse2 = NullPerson()
		self.children = list()
		self.date = ''
		self.place = ''

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

	def toHTML(self):
		to_html = (
			'<div class="union">\n'
			'  {}\n'
			'  <div class="date">{}</div>\n'
			'  {}\n'
			'</div>\n'
		).format(self.spouse1.toHTML(), self.date, self.spouse2.toHTML())
		return to_html

	def __str__(self):
		to_str = "{{ {} & {} }}".format(self.spouse1, self.spouse2)
		return to_str
