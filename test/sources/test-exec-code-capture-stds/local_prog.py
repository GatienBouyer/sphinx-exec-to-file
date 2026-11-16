#!/usr/bin/python3
"""Code that reproduce a user's program to be used in our tests."""

import sys

sys.stdout.write('"Treat", "Quantity", "Description"\n')
sys.stdout.flush()
sys.stderr.write('"Albatross", 2.99, "On a stick!"\n')
sys.stderr.flush()
sys.stdout.write('"Crunchy Frog", 1.49, "If we took the bones out,\n'
                 'it wouldn\'t be crunchy, now would it?"\n')
sys.stdout.flush()
sys.stderr.write('"Gannet Ripple", 1.99, "On a stick!"\n')
