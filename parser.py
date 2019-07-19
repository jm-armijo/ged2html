from person import Person

class Parser():
	def __init__(self):
		self.people = list()
		self.is_person = False
		self.line = None

	def parseLines(self, lines):
		for self.current_line in lines:
			self.parseCurrentLine()

		return self.people

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
		value  = self.current_line.data

		if attribute == 'NAME':
			person.addName(level, value)
		else:
			person.addAttribute(level, attribute, value)
