"""Test the extension."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

# pylint: disable=duplicate-code


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-capture-saved-in-folder",
)
def test_capture_saved_in_folder(app: SphinxTestApp, ref_path: Path) -> None:
    """Test in which the file is saved inside a directory, that needs to be created."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-capture-multiple-files",
)
def test_capture_multiple_files(app: SphinxTestApp, ref_path: Path) -> None:
    """Test in which the script called generated multiple files."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table-multiple")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-capture-stdout",
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
    testroot="exec-code-capture-stderr",
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
    testroot="exec-code-capture-stds",
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
    testroot="exec-code-file-not-created",
)
def test_file_not_created(app: SphinxTestApp) -> None:
    """Test in which the script called does not create the captured file."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: WARNING: Command executed but didn't create the file data.csv:"
    assert msg in warnings


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-file-not-in-code",
)
def test_file_not_in_code(app: SphinxTestApp) -> None:
    """Test in which the code does not use a captured file."""
    app.build()
    warnings = app.warning.getvalue()
    msg = ("index.rst:1: WARNING: 'exec:code' does not use 'data.csv' in the command:\n"
           "prog.py --option")
    assert msg in warnings


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-file-not-in-capture",
)
def test_file_not_in_capture(app: SphinxTestApp) -> None:
    """Test in which the code used a file not defined in captures."""
    app.build()
    warnings = app.warning.getvalue()
    msg = ("index.rst:1: WARNING: 'exec:code' does not define the capture of '<data.csv>' "
           "for the command:\nprog.py <data.csv>")
    assert msg in warnings


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-file-twice-in-capture",
)
def test_file_twice_in_capture(app: SphinxTestApp) -> None:
    """Test in which the code used a file defined twice in the capture option."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: WARNING: duplicate file 'data.csv' in 'exec:code' captured twice"
    assert msg in warnings


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-file-twice-in-capture-stdout",
)
def test_file_twice_in_capture_stdout(app: SphinxTestApp) -> None:
    """Test in which the code used a file defined twice in the capture option."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: WARNING: duplicate file 'data.csv' in 'exec:code' captured twice"
    assert msg in warnings


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-file-twice-in-capture-stderr",
)
def test_file_twice_in_capture_stderr(app: SphinxTestApp) -> None:
    """Test in which the code used a file defined twice in the capture option."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: WARNING: duplicate file 'data.csv' in 'exec:code' captured twice"
    assert msg in warnings
