from src.html import HTMLGenerator
from src.tree_node import TreeNode

class TreeLevel():
	def __init__(self):
		self.nodes = list()

	def append(self, node):
		node = TreeNode(node)
		self.nodes.append(node)

	def toHTML(self):
		value = HTMLGenerator.listToHTML(self.nodes)
		return HTMLGenerator.wrap(self, value)
