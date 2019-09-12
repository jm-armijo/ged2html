"""
Entry point script that creates an html file
for a given .ged file.
"""

import os
import sys
from shutil import copyfile
from src.html import HTMLGenerator
from src.parser import Parser

def generate_html_document(file_name):
    parser = Parser()
    tree = parser.make_tree(file_name)
    html_tree = tree.to_html()

    title = "My Genealogy Tree"
    doc = HTMLGenerator('html/index.html')
    doc.generate(title, html_tree)

def create_output_directory():
    # Make directories
    os.makedirs('html/css', 755, True)
    os.makedirs('html/scripts', 755, True)

    # Copy files
    copyfile('src/css/styles.css', 'html/css/styles.css')
    copyfile('src/scripts/leader-line.min.js', 'html/scripts/leader-line.min.js')

def are_args_valid():
    num_args = len(sys.argv)
    if num_args != 2:
        print("Expected 1 argument, received {}".format(num_args -1))
        return False
    else:
        return True

if are_args_valid():
    file_name = sys.argv[1]
    create_output_directory()
    generate_html_document(file_name)

