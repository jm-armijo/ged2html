import re

class Node():
	def __init__(self, level, key, value):
		self.level = level
		self.key = key
		self.children = list()
		self.value = value

	def addNode(self, attribute):
		if attribute.level == self.level + 1:
			self.children.append(attribute)
		else:
			self.children[-1].addNode(attribute)

	def __bool__(self):
		if self.value != "":
			return True

		for child in self.children:
			if child:
				return True

		return False


	def __getitem__(self, index):
		return self.children[index]

	def __str__(self):
		to_str = " " * self.level + self.key
		if self.value != "":
			to_str += " : " + self.value

		for child in self.children:
			to_str += "\n" + child.__str__()

		return to_str

class Person(Node):
	def __init__(self, id):
		super().__init__(0, 'ID', id)

	def addAttribute(self, level, attribute, value):
		attribute = Node(level, attribute, value)
		super().addNode(attribute)

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
		person = Person(self.current_line.attribute)
		self.people.append(person)
		self.is_person = True
		
	def addPersonData(self):
		person = self.people[-1]
		level = int(self.current_line.level)
		attribute = self.current_line.attribute
		data  = self.current_line.data

		if attribute == 'NAME':
			name = self.getPersonName(data)
			person.addAttribute(level, 'NAME', name['NAME'])
			person.addAttribute(level+1, 'GIVN', name['GIVN'])
		else:
			person.addAttribute(level, attribute, data)

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
		print(self.people[idx])

# Read the file into a list of lines
def readFile(file_name):
	with open(file_name,mode='r') as tree_file:
		return map(Line, tree_file.readlines())

lines = readFile('tree.ged')
parser = Parser()
parser.parseLines(lines)
parser.printPerson(3)
