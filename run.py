from src.parser import Parser

file_name = 'tree.ged'
parser = Parser()
tree = parser.makeTree(file_name)
tree.toHTML('html/index.html')
