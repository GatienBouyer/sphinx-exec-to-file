"""Test the exec-file directive."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

# pylint: disable=duplicate-code


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-capture-stdout",
)
def test_capture_stdout(app: SphinxTestApp, ref_path: Path) -> None:
    """Test the capture of the stdout of the script called."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-capture-stderr",
)
def test_capture_stderr(app: SphinxTestApp, ref_path: Path) -> None:
    """Test the capture of the stderr of the script called."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-capture-stds",
)
def test_capture_both(app: SphinxTestApp, ref_path: Path) -> None:
    """Test the capture of the stdout and stderr of the script called,
    while keeping the text order."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-file-not-found",
)
def test_file_not_found(app: SphinxTestApp) -> None:
    """Test in which the script to run does not exists."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: CRITICAL: Failed to found the file to execute:"
    assert msg in warnings


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-file-not-in-code",
)
def test_file_not_in_code(app: SphinxTestApp) -> None:
    """Test in which the code does not use a captured file."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: WARNING: 'exec:file' does not use 'data.csv' in the file:"
    assert msg in warnings
