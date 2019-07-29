class Node():
	def __init__(self, level, key, value):
		self.level = level
		self.key = key
		self.value = value
		self.children = list()
		self.last_child = None

	def addNode(self, attribute):
		if attribute.level > self.level + 1:
			idx = self.last_child
			self.children[idx].addNode(attribute)
		else:
			self.last_child = len(self.children)
			self.children.append(attribute)

	def __getitem__(self, index):
		return self.children[index]

	def __str__(self):
		to_str = " " * self.level + self.key
		if self.value != "":
			to_str += " : " + self.value

		for child in self.children:
			to_str += "\n" + child.__str__()

		return to_str

