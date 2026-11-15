#!/usr/bin/python3
"""Code that reproduce a user's program to be used in our tests."""
import sys

output_file1 = sys.argv[1]

with open(output_file1, "w", encoding="utf-8") as file:
    file.writelines([
        '"Treat", "Quantity", "Description"\n',
        '"Albatross", 2.99, "On a stick!"\n',
    ])

output_file2 = sys.argv[2]

with open(output_file2, "w", encoding="utf-8") as file:
    file.writelines([
        '"Treat", "Quantity", "Description"\n',
        '"Gannet Ripple", 1.99, "On a stick!"\n',
    ])
