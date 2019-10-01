"""
Entry point script that creates an html file
for a given .ged file.
"""

import os
import sys
from shutil import copyfile
from src.html import HTMLGenerator
from src.parser import Parser

def generate_html_document(file_name, title='Family Tree'):
    parser = Parser()
    tree = parser.make_tree(file_name)
    html_tree = tree.to_html()

    doc = HTMLGenerator('html/index.html')
    doc.generate(title, html_tree)

def create_output_directory():
    # Make directories
    os.makedirs('html/css', 755, True)
    os.makedirs('html/scripts', 755, True)
    os.makedirs('html/images', 755, True)

    # Copy files
    copyfile('src/css/styles.css', 'html/css/styles.css')
    copyfile('src/scripts/leader-line.min.js', 'html/scripts/leader-line.min.js')
    copyfile('src/images/face.png', 'html/images/face.png')
    copyfile('src/images/unionlink.png', 'html/images/unionlink.png')
    copyfile('src/images/bg.jpg', 'html/images/bg.jpg')
    copyfile('src/images/sex-M.png', 'html/images/sex-M.png')
    copyfile('src/images/sex-F.png', 'html/images/sex-F.png')
    copyfile('src/images/scroll.png', 'html/images/scroll.png')

def are_args_valid():
    num_args = len(sys.argv)
    if num_args != 3:
        print("Expected 2 argument, received {}".format(num_args -1))
        return False
    else:
        return True

if are_args_valid():
    file_name = sys.argv[1]
    title = sys.argv[2]
    create_output_directory()
    generate_html_document(file_name, title)

