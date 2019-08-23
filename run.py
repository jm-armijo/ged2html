from src.html import HTMLDocument
from shutil import copyfile
import os

from src.parser import Parser

# Make directories
os.makedirs('html/css', 755, True);
os.makedirs('html/scripts', 755, True);

# Copy files
copyfile('src/css/styles.css', 'html/css/styles.css')
copyfile('src/scripts/leader-line.min.js', 'html/scripts/leader-line.min.js')

file_name = 'tree.ged'
parser = Parser()
tree = parser.makeTree(file_name)
html_tree = tree.toHTML()

title = "My Genealogy Tree"
doc = HTMLDocument('html/index.html')
to_html = doc.generate(title, html_tree)
