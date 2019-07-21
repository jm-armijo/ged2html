from src.node import Node
import re

class Person(Node):
	def __init__(self, id):
		super().__init__(0, 'ID', id)

	def addName(self, level, value):
		match = re.search('(.*)/(.*)/', value)
		if match:
			self.addAttribute(level, 'NAME', match.group(2).strip())
			self.addAttribute(level+1, 'GIVN', match.group(1).strip())
		else:
			print("raise error!")

	def addAttribute(self, level, attribute, value):
		attribute = Node(level, attribute, value)
		super().addNode(attribute)

