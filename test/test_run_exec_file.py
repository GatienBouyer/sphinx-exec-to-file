"""Test the execution of the code given to the exec-file directive."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

# pylint: disable=duplicate-code


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-local-script",
)
def test_local_script(app: SphinxTestApp, ref_path: Path) -> None:
    """Test to exec a script that is next to the conf.py."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-lang-python",
)
def test_language_python(app: SphinxTestApp, ref_path: Path) -> None:
    """Test to exec a python script that is next to the conf.py."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-config-runners",
)
def test_language_custom(app: SphinxTestApp, ref_path: Path) -> None:
    """Test the exec_file_runners extension configuration option."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-no-file",
)
def test_no_code(app: SphinxTestApp) -> None:
    """Test in which the file to be run is missing form the directive argument."""
    app.build()
    warnings = app.warning.getvalue()
    msg = 'index.rst:1: ERROR: Error in "exec:file" directive:\n1 argument(s) required, 0 supplied'
    assert msg in warnings
