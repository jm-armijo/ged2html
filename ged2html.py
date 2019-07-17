import re

class Node():
	def __init__(self, key, value):
		self.key = key
		self.children = list()
		self.value = value

	def append(self, node):
		self.children.append(node)

	def __getitem__(self, index):
		return self.children[index]

	def __str__(self):
		text = self.key + " : " + self.value
		for child in self.children:
			text += "\n" + child.__str__()

		return text

class Person():
	def __init__(self):
		self.fields = list()

	def setField(self, level, field, value):
		new_node = Node(field, value)
		parent_node = self.getParentForNewNode(level)
		parent_node.append(new_node)

	def getParentForNewNode(self, level):
		node = self.fields
		for i in range(level-1):
			node = node[-1]
		return node

	def print(self):
		for node in self.fields:
			print(str(node))

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
		level = int(self.current_line.level)
		field = self.current_line.field
		data  = self.current_line.data

		if field == 'NAME':
			name = self.getPersonName(data)
			person.setField(level, 'NAME', name['NAME'])
			person.setField(level+1, 'GIVN', name['GIVN'])
		else:
			person.setField(level, field, data)

	def getPersonName(self, data):
		match = re.search('(.*)/(.*)/', data)
		name = dict()
		if match:
			name['GIVN'] = match.group(1).strip()
			name['NAME'] = match.group(2).strip()
		else:
			print("raise error!")

		return name

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
