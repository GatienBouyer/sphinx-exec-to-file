#!/usr/bin/python3
"""Code that reproduce a user's program to be used in our tests."""
import sys

output_file = sys.argv[1]

with open(output_file, "w", encoding="utf-8") as file:
    # pylint: disable=duplicate-code
    file.writelines([
        '"Treat", "Quantity", "Description"\n',
        '"Albatross", 2.99, "On a stick!"\n',
        '"Crunchy Frog", 1.49, "If we took the bones out,\n',
        'it wouldn\'t be crunchy, now would it?"\n'
        '"Gannet Ripple", 1.99, "On a stick!"\n',
    ])
