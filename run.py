"""
Entry point script that creates an html file
for a given .ged file.
"""

import os
from shutil import copyfile
from src.html import HTMLGenerator
from src.parser import Parser

# Make directories
os.makedirs('html/css', 755, True)
os.makedirs('html/scripts', 755, True)

# Copy files
copyfile('src/css/styles.css', 'html/css/styles.css')
copyfile('src/scripts/leader-line.min.js', 'html/scripts/leader-line.min.js')

file_name = '../tree.ged'
parser = Parser()
tree = parser.makeTree(file_name)
html_tree = tree.toHTML()

title = "My Genealogy Tree"
doc = HTMLGenerator('html/index.html')
doc.generate(title, html_tree)
