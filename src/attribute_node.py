class AttributeNode():
	def __init__(self, level, key, value):
		self.level = level
		self.key = key
		self.value = value
		self.children = dict()
		self.last_child = None

	def pickParent(self, attribute):
		if attribute.level > self.level + 1:
			child = self.children[self.last_child]
			return child.pickParent(attribute)
		return self

	def addChildAttribute(self, level, key, value):
		attribute = AttributeNode(level, key, value)
		self.appendAttribute(attribute)

	def appendAttribute(self, attribute):
		parent = self.pickParent(attribute)
		parent.last_child = attribute.key

		if attribute.key in parent.children:
			child = parent.children[attribute.key]
			child.value = max((child.value, attribute.value))
		else:
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

