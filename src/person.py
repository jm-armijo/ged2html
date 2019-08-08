import re
from src.node import Node

class Person(Node):
	def __init__(self, id):
		super().__init__(0, 'ID', id)

	def addAttribute(self, level, key, value):
		if key == 'NAME':
			self.addName(level, key, value)
		else:
			super().addNode(level, key, value)

	def addName(self, level, key, value):
		name = self.splitName(value)

		super().addNode(level, key, '')
		super().addNode(level + 1, 'GIVN', name[0])
		super().addNode(level + 1, 'LAST', name[1])

	def splitName(self, name):
		match = re.search('^(.*?)/(.*?)/?\s*$', name)
		if match:
			return (match.group(1).strip(), match.group(2).strip())
		else:
			print("raise error!")
