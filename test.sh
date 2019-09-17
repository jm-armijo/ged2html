#!/bin/bash

printf "\n\nRunning Line tests...\n"
python3 -m unittest src.tests.text_line

printf "\n\nRunning Node tests...\n"
python3 -m unittest src.tests.node

printf "\n\nRunning Union tests...\n"
python3 -m unittest src.tests.union

printf "\n\nRunning UnionLink tests...\n"
python3 -m unittest src.tests.union_link

printf "\n\nRunning Person tests...\n"
python3 -m unittest src.tests.person

printf "\n\nRunning Parser tests...\n"
python3 -m unittest src.tests.parser

printf "\n\nRunning Tree tests...\n"
python3 -m unittest src.tests.tree

printf "\n\nRunning TreeLevel tests...\n"
python3 -m unittest src.tests.tree_level

printf "\n\nRunning TreeNode tests...\n"
python3 -m unittest src.tests.tree_node

printf "\n\nRunning unique_queue tests...\n"
python3 -m unittest src.tests.unique_queue

printf "\n\nRunning Edge tests...\n"
python3 -m unittest src.tests.edge

printf "\n\nRunning HTMLGenerator tests...\n"
python3 -m unittest src.tests.html

printf "\n\nRunning Date tests...\n"
python3 -m unittest src.tests.date
