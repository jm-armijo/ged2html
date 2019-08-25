from src.html import HTMLGenerator

class TreeNode():
	def __init__(self, node):
		self.node = node
	
	def toHTML(self):
		value = self.node.toHTML()
		return HTMLGenerator.wrap(self, value)
