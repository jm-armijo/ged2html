import re

class Person():
	def __init__(self):
		self.fields = {}

	def setName(self, level, data):
		match = re.search('(.*)/(.*)/', data)
		if match:
			self.setField(level, 'GIVN', match.group(1).strip())
			self.setField(level, 'NAME', match.group(2).strip())
		else:
			print("raise error!")

	def setField(self, level, field, value):
		self.fields[field] = value

	def print(self):
		print(self.fields)

class Line():
	def __init__(self, line):
		self.line = line
		self.parseLine(line)
	
	def parseLine(self, line):
		parts = line.split()
		self.level = parts[0]
		self.field = parts[1]
		if len(parts) > 2:
			self.data = line[len(self.level)+len(self.field)+2:].rstrip()
		else:
			self.data = ''
	
	def isPersonHeader(self):
		if self.level == '0' and self.data == 'INDI':
			print('HEADER FOUND ' + self.field)
			return True

	def isInfo(self):
		if self.level > '0':
			return True

class Parser():
	def __init__(self):
		self.people = list()
		self.is_person = False
		self.line = None

	def parseLines(self, lines):
		for self.current_line in lines:
			self.parseCurrentLine()

	def parseCurrentLine(self):
		if self.current_line.isPersonHeader():
			self.createPerson()
		elif self.is_person and self.current_line.isInfo():
			self.addPersonData()
		else:
			self.is_person = False
	
	def createPerson(self):
		person = Person()
		self.people.append(person)
		self.is_person = True
		
	def addPersonData(self):
		person = self.people[-1]
		level = self.current_line.level
		field = self.current_line.field
		data  = self.current_line.data

		if field == 'NAME':
			person.setName(level, data)
		else:
			person.setField(level, field, data)

	def printPerson(self, idx):
		self.people[idx].print()

# Read the file into a list of lines
def readFile(file_name):
	with open(file_name,mode='r') as tree_file:
		return map(Line, tree_file.readlines())

lines = readFile('tree.ged')
parser = Parser()
parser.parseLines(lines)
parser.printPerson(2)
