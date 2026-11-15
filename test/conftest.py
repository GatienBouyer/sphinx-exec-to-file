"""Pytest fixtures."""
from os import environ
from pathlib import Path

import pytest

pytest_plugins = ["sphinx.testing.fixtures"]


@pytest.fixture(name="rootdir", scope="session")
def sphinx_rootdir() -> Path:
    """Configure the Sphinx testing app"""
    root_dir = Path(__file__).parent / "sources"

    # Add the user script to the path
    # in a real scenario, the script would be already by in the user's path
    path = environ.get("PATH", "")
    userland_progs = root_dir / "userland-progs"
    environ["PATH"] = f"{path}:{userland_progs}"

    return root_dir


@pytest.fixture(name="ref_path", scope="session")
def ref_path_fixture() -> Path:
    """Return the path containing the output reference."""
    return Path(__file__).parent / "expected_outputs"
