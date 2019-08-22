from src.node import Node

class NullPerson(Node):
	def toHTML(self):
		return '<div class="person"></div>'
	
	def getUnions(self):
		return list()

