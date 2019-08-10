from src.person import Person
from src.union import Union

class Parser():
	def __init__(self):
		self.people = dict()
		self.current_line = None
		self.state = 'IDLE'
		self.last_person = None

		self.last_key_per_level = dict()
		self.unions = list()

	def parseLines(self, lines):
		for self.current_line in lines:
			self.last_key_per_level[self.current_line.level] = self.current_line.attribute
			self.state = self.getCurrentState()
			self.parseCurrentLine()

		return self.people


	'''
	getCurrentState: implements the state machine below
	in: current state
	returns: new state

	############################################
	#                                          #
	#                    *         +-----+     #
	#                    |         |     |     #
	#                    V         |     V     #
	#             +--->(INDI) -> (INDI_DATA)   #
	#             |                            #
	#   * ---> (IDLE)                          #
	#             |                            #
	#             +--->(FAM)  -> (FAM_DATA)    #
	#                    /\        |     /\    #
	#                    |         |     |     #
	#                    *         +-----+     #
	#                                          #
	############################################
	'''

	def getCurrentState(self):
		new_state = 'IDLE'
		if self.current_line.level == 0 and self.current_line.data in ['INDI', 'FAM']:
			new_state = self.current_line.data
		elif self.state == 'INDI' or self.state == 'INDI_DATA':
			if self.current_line.level > 0:
				new_state = 'INDI_DATA'
		elif self.state == 'FAM' or self.state == 'FAM_DATA':
			if self.current_line.level > 0:
				new_state = 'FAM_DATA'

		return new_state

	def parseCurrentLine(self):
		if self.state == 'INDI':
			self.createPerson()
		elif self.state == 'INDI_DATA':
			self.addPersonData()
		elif self.state == 'FAM':
			self.createUnion()
		elif self.state == 'FAM_DATA':
			self.addUnionData()

	def createPerson(self):
		person = self.getPersonOrCreate(self.current_line.attribute)
		self.people[person.id] = person
		self.last_person = person.id

	def addPersonData(self):
		level = self.current_line.level
		attribute = self.current_line.attribute
		value  = self.current_line.data

		person = self.people[self.last_person]

		if attribute == 'NAME':
			person.setName(value)
		elif attribute == 'GIVN':
			person.setGivenName(value)
		elif attribute == 'SEX':
			person.setSex(value)
		elif attribute == 'DATE' and self.last_key_per_level[level - 1] == 'BIRT':
			person.setBirthDate(value)
		elif attribute == 'PLAC' and self.last_key_per_level[level - 1] == 'BIRT':
			person.setBirthPlace(value)

	def createUnion(self):
		self.unions.append(Union(self.current_line.attribute))

	def addUnionData(self):
		level = self.current_line.level
		attribute = self.current_line.attribute
		value  = self.current_line.data

		union = self.unions[-1]

		if attribute == 'HUSB':
			union.setSpouse1(self.getPersonOrCreate(value))
		elif attribute == 'WIFE':
			union.setSpouse2(self.getPersonOrCreate(value))
		elif attribute == 'CHIL':
			union.addChild(self.getPersonOrCreate(value))
		elif attribute == 'DATE' and self.last_key_per_level[level - 1] == 'MARR':
			union.setDate(value)
		elif attribute == 'PLAC' and self.last_key_per_level[level - 1] == 'MARR':
			union.setPlace(value)

	def getPersonOrCreate(self, id):
		if id not in self.people:
			self.people[id] = Person(id)

		return self.people[id]
