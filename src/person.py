from src.node import Node
import re

class Person(Node):
	def __init__(self, id):
		self.id = id
		self.given_name = ''
		self.last_name = ''
		self.sex = ''
		self.birth_date = ''
		self.birth_place = ''
		self.death_date = ''
		self.death_place = ''
		self.parents = None
		self.unions = list()

	def setName(self, name):
		name_parts = self._splitName(name)
		self.setGivenName(name_parts[0] )
		self.last_name = name_parts[1]

	def setGivenName(self, given_name):
		if self.given_name == '':
			self.given_name = given_name

	def setSex(self, sex):
		self.sex = sex

	def setBirthDate(self, date):
		self.birth_date = date

	def setBirthPlace(self, place):
		self.birth_place = place

	def setDeadthDate(self, date):
		self.death_date = date

	def setDeadthPlace(self, place):
		self.death_place = place

	def setParents(self, parents):
		self.parents = parents

	def addUnion(self, union):
		self.unions.append(union)

	def getChildren(self):
		children = list()
		for union in self.unions:
			children += union.getChildren()
		return children

	def getParents(self):
		if self.parents is None:
			return list()
		else:
			return [self.parents]

	def getUnions(self):
		return self.unions

	def isSingle(self):
		return len(self.unions) == 0

	def _splitName(self, name):
		match = re.search('^(.*?)/(.*?)/?\s*$', name)
		if match:
			return (match.group(1).strip(), match.group(2).strip())
		else:
			print("raise error!")

	def __str__(self):
		return "[{} {}]".format(self.given_name, self.last_name)
