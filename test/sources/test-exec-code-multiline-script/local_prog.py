#!/usr/bin/python3
"""Code that reproduce a user's program to be used in our tests."""
import sys

expected_args = [
    "local_prog.py",
    "--there-is-too-many",
    "--too-many-options-to-keep-it-in-single-line",
    "--here-is-a-multiline-shell-command",
]

sys.stdout.write("\n" + "\n".join(sys.argv) + "\n")

assert len(sys.argv) == len(expected_args)
assert sys.argv[2:] == expected_args[2:]
