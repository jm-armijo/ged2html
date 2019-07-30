class Node():
	def __init__(self, level, key, value):
		self.level = level
		self.key = key
		self.value = value
		self.children = dict()
		self.last_child = None

	def pickParent(self, attribute):
		if attribute.level > self.level + 1:
			key = self.last_child
			return self.children[key].pickParent(attribute)
		return self

	def addNode(self, attribute):
		parent = self.pickParent(attribute)
		parent.last_child = attribute.key
		parent.children[attribute.key] = attribute

	def __getitem__(self, index):
		return self.children[index]

	def __str__(self):
		to_str = " " * self.level + self.key
		if self.value != "":
			to_str += " : " + self.value

		for child in self.children.values():
			to_str += "\n" + child.__str__()

		return to_str

