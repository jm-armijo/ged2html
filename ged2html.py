from line import Line
from parser import Parser

# Read the file into a list of lines
def readFile(file_name):
	with open(file_name,mode='r') as tree_file:
		return map(Line, tree_file.readlines())

lines = readFile('tree.ged')
parser = Parser()
people = parser.parseLines(lines)
for person in people:
	print(person)
	print()
