class Line():
	def __init__(self, line):
		self.line = line
		self.parseLine(line)
	
	def parseLine(self, line):
		parts = line.split()
		self.level = int(parts[0])
		self.attribute = parts[1]
		if len(parts) > 2:
			self.data = line[len(parts[0])+len(self.attribute)+2:].rstrip()
		else:
			self.data = ''
