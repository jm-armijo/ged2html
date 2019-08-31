from src.node import Node

class NullPerson(Node):
	def to_html(self):
		return '<div class="person"></div>'
	
	def get_unions(self):
		return list()

