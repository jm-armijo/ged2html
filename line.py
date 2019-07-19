class Line():
	def __init__(self, line):
		self.line = line
		self.parseLine(line)
	
	def parseLine(self, line):
		parts = line.split()
		self.level = parts[0]
		self.attribute = parts[1]
		if len(parts) > 2:
			self.data = line[len(self.level)+len(self.attribute)+2:].rstrip()
		else:
			self.data = ''
	
	def isPersonHeader(self):
		if self.level == '0' and self.data == 'INDI':
			return True

	def isInfo(self):
		if self.level > '0':
			return True
