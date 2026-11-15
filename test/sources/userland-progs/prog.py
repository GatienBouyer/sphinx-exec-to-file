#!/usr/bin/python3
"""Code that reproduce a user's program to be used in our tests."""
import argparse
from collections.abc import Sequence
from pathlib import Path


class Args:
    """Contains the parsed arguments of the program as attributes."""
    output: Path

    @staticmethod
    def config_parser(parser: argparse.ArgumentParser) -> None:
        """Configure the argument parser in accordance with the defined attributes."""
        parser.add_argument("output", type=Path)


def main(argv: Sequence[str] | None = None) -> None:
    """Main process of the program."""
    parser = argparse.ArgumentParser()
    Args.config_parser(parser)
    args = parser.parse_args(argv, Args())

    with args.output.open("w") as file:
        file.writelines([
            '"Treat", "Quantity", "Description"\n',
            '"Albatross", 2.99, "On a stick!"\n',
            '"Crunchy Frog", 1.49, "If we took the bones out,\n',
            'it wouldn\'t be crunchy, now would it?"\n'
            '"Gannet Ripple", 1.99, "On a stick!"\n',
        ])


if __name__ == "__main__":
    main()
