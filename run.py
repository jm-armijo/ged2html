"""
Entry point script that creates an html file
for a given .ged file.
"""

import os
import sys
from shutil import copyfile
from src.html_tree import HTMLTree
from src.html_profile import HTMLProfile
from src.parser import Parser

def copy_media_files(base_path, media_files):
    for file in media_files:
        if 'docs/' not in file:
            origin = os.path.join(base_path,file)
            copyfile(origin, 'html/' + file )

def write_to_file(file_name, content):
    file_handler = open(file_name, 'w')
    file_handler.write(content)
    file_handler.close()

def generate_html_documents(file_name, title='Family Tree'):
    parser = Parser()
    parser.parse(file_name)
    media_files = parser.get_media_files()
    tree = parser.make_tree()

    base_path = os.path.dirname(file_name)
    copy_media_files(base_path, media_files)

    # Generate the main document with the tree structure
    doc = HTMLTree(title, tree)
    html = doc.get_document()

    output_index_file = 'html/index.html'
    write_to_file(output_index_file, html)

    # Generate one document with the profile of each person
    people = parser.people
    for person in people.values():
        dir = person.id
        os.makedirs('html/'+dir, 0o755, True)

        doc = HTMLProfile(title, person)
        html = doc.get_document()

        output_profile_file = 'html/{}/index.html'.format(dir)
        write_to_file(output_profile_file, html)

def create_output_directory():
    # Make directories
    os.makedirs('html/css', 0o755, True)
    os.makedirs('html/scripts', 0o755, True)
    os.makedirs('html/images', 0o755, True)

    # Copy files
    copyfile('src/css/base.css', 'html/css/base.css')
    copyfile('src/css/tree.css', 'html/css/tree.css')
    copyfile('src/css/profile.css', 'html/css/profile.css')
    copyfile('src/scripts/leader-line.min.js', 'html/scripts/leader-line.min.js')
    copyfile('src/images/face.png', 'html/images/face.png')
    copyfile('src/images/unionlink.png', 'html/images/unionlink.png')
    copyfile('src/images/sex-M.png', 'html/images/sex-M.png')
    copyfile('src/images/sex-F.png', 'html/images/sex-F.png')
    copyfile('src/images/icon.png', 'html/images/icon.png')

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
    generate_html_documents(file_name, title)

