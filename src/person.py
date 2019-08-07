import re
from src.node import Node

class Person(Node):
	def __init__(self, id):
		super().__init__(0, 'ID', id)

	def addAttribute(self, level, key, value):
		attribute = Node(level, key, value)

		if key == 'NAME':
			self.addName(attribute)
		else:
			super().addNode(attribute)

	def addName(self, attribute):
		name = self.splitName(attribute.value)

		attr_name = Node(attribute.level, attribute.key, '')
		super().addNode(attr_name)

		attr_givn = Node(attribute.level + 1, 'GIVN', name[0])
		super().addNode(attr_givn)

		attr_last = Node(attribute.level + 1, 'LAST', name[1])
		super().addNode(attr_last)

	def splitName(self, name):
		match = re.search('^(.*?)/(.*?)/?\s*$', name)
		if match:
			return (match.group(1).strip(), match.group(2).strip())
		else:
			print("raise error!")
