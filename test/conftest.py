"""Pytest fixtures."""
from pathlib import Path
from shutil import copytree

import pytest

pytest_plugins = ["sphinx.testing.fixtures"]


@pytest.fixture(name="rootdir", scope="session")
def sphinx_rootdir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Configure the Sphinx testing app"""
    src = Path(__file__).parent / "sources"
    dst = tmp_path_factory.mktemp("sphinx-tests") / "docs"
    copytree(src, dst)
    return dst


@pytest.fixture(name="ref_path", scope="session")
def ref_path_fixture() -> Path:
    """Return the path containing the output reference."""
    return Path(__file__).parent / "expected_outputs"
