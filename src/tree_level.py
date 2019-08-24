from src.html import HTMLGenerator
from src.tree_node import TreeNode

class TreeLevel():
	def __init__(self):
		self.category = 'level'
		self.nodes = list()

	def append(self, node):
		node = TreeNode(node)
		self.nodes.append(node)

	def toHTML(self):
		value = self._nodesToHTML(self.nodes)
		return HTMLGenerator.wrap(self.category, value)

	def _nodesToHTML(self, nodes):
		html_nodes = ''
		for node in nodes:
			html_nodes += node.toHTML()
		return html_nodes
