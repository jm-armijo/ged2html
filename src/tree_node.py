from src.html import HTMLGenerator

class TreeNode():
	def __init__(self, node):
		self.category = 'node'
		self.node = node
	
	def toHTML(self):
		value = self.node.toHTML()
		return HTMLGenerator.wrap(self.category, value)
