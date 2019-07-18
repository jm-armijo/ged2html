import re

class Attribute():
	def __init__(self, level, key, value):
		self.level = level
		self.key = key
		self.children = list()
		self.value = value

	def append(self, attribute):
		self.children.append(attribute)

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

class Person():
	def __init__(self):
		self.attributes = list()

	def setAttribute(self, level, attribute, value):
		new_attribute = Attribute(level, attribute, value)
		parent_attribute = self.getParentForNewAttribute(level)
		parent_attribute.append(new_attribute)

	def getParentForNewAttribute(self, level):
		attribute = self.attributes
		for i in range(level-1):
			attribute = attribute[-1]
		return attribute

	def __str__(self):
		to_str = ""
		for attribute in self.attributes:
			if attribute:
				to_str += str(attribute) + "\n"

		return to_str

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
		person = Person()
		self.people.append(person)
		self.is_person = True
		
	def addPersonData(self):
		person = self.people[-1]
		level = int(self.current_line.level)
		attribute = self.current_line.attribute
		data  = self.current_line.data

		if attribute == 'NAME':
			name = self.getPersonName(data)
			person.setAttribute(level, 'NAME', name['NAME'])
			person.setAttribute(level+1, 'GIVN', name['GIVN'])
		else:
			person.setAttribute(level, attribute, data)

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
