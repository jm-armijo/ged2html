class Edge():
	def __init__(self, start, end):
		self.start = start
		self.end = end
	
	def toHTML(self):
		return (
			'        new LeaderLine(\n'
			'          document.getElementById("{}"),\n'
			'          document.getElementById("{}"),\n'
			'        );\n'
		).format(self.start, self.end)
