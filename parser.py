from person import Person

class Parser():
	def __init__(self):
		self.people = list()
		self.is_person = False
		self.line = None

	def parseLines(self, lines):
		state = 'idle'
		for self.current_line in lines:
			state = self.getCurrentState(state)
			self.parseCurrentLine(state)

		return self.people


	'''
	getCurrentState: implements the state machine below
	in: current state
	returns: new state

	###########################################################
	#
	#             +----------------------------------+
	#             V                                  |
	# (idle) -> (ind) -> (ind_data) -> (fam) -> (fam_data)
	#   |         /\         |          /\   /\      |
	#   |         +----------+          |    +-------+
	#   +-------------------------------+
	#
	###########################################################
	'''

	def getCurrentState(self, current_state):
		new_state = 'idle'
		if self.current_line.level == 0:
			new_state = self.current_line.data
		elif current_state == 'INDI' or current_state == 'INDI_DATA':
			if self.current_line.level > 0:
				new_state = 'INDI_DATA'
		elif current_state == 'FAM' or current_state == 'FAM_DATA':
			if self.current_line.level > 0:
				new_state = 'FAM_DATA'

		return new_state

	def parseCurrentLine(self, state):
		if state == 'INDI':
			self.createPerson()
		elif state == 'INDI_DATA':
			self.addPersonData()
		elif state == 'FAM':
			pass
		elif state == 'FAM_DATA':
			pass
	
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
