import re

class Person():
	def __init__(self):
		self.tags = {}

	def addTag(self,name,value):
		self.tags[name] = value

	def print(self):
		print(self.tags)

class Line():
	def __init__(self, line):
		self.line = line
		self.parseLine(line)
	
	def parseLine(self, line):
		parts = line.split()
		self.code = parts[0]
		self.tag = parts[1]
		if len(parts) > 2:
			self.data = line[len(self.code)+len(self.tag)+2:].rstrip()
		else:
			self.data = ''
	
	def isPersonHeader(self):
		if self.code == '0' and self.data == 'INDI':
			print('HEADER FOUND ' + self.tag)
			return True

	def isInfo(self):
		if self.code > '0':
			return True

class Parser():
	def __init__(self):
		self.people = list()
		self.is_person = False

	def parseLines(self,lines):
		for line in lines:
			self.parseLine(line)

	def parseLine(self, line):
		line_obj = Line(line)

		if line_obj.isPersonHeader():
			self.createPerson()
		elif self.is_person and line_obj.isInfo():
			self.addPersonData(line_obj.tag, line_obj.data)
		else:
			self.is_person = False
	
	def createPerson(self):
		person = Person()
		self.people.append(person)
		self.is_person = True
		
	def addPersonData(self, key, value):
		if key == 'NAME':
			self.addPersonName(value)
		else:
			person = self.people[-1]
			person.addTag(key,value)

	def addPersonName(self, value):
		person = self.people[-1]

		match = re.search('(.*)/(.*)/', value)
		if match:
			person.addTag('GIVN', match.group(1).strip())
			person.addTag('NAME', match.group(2).strip())
		else:
			print("raise error!")

	def printPerson(self, idx):
		self.people[idx].print()

# Read the file into a list of lines
def readFile(file_name):
	with open(file_name,mode='r') as tree_file:
		return tree_file.readlines()


lines = readFile('tree.ged')
parser = Parser()
parser.parseLines(lines)
parser.printPerson(2)
