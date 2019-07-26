from src.node import Node

class Person(Node):
	def __init__(self, id):
		super().__init__(0, 'ID', id)

	def addAttribute(self, level, attribute, value):
		attribute = Node(level, attribute, value)
		super().addNode(attribute)

