"""Test the extension."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

# pylint: disable=duplicate-code


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-capture-into-subdir",
)
def test_capture_file_subdir(app: SphinxTestApp, ref_path: Path) -> None:
    """Test in which the file is saved inside a directory, that needs to be created."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "hello-world")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-capture-into-subdir-stdout",
)
def test_capture_stdout_subdir(app: SphinxTestApp, ref_path: Path) -> None:
    """Test in which the file is saved inside a directory, that needs to be created."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "hello-world")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-capture-into-subdir-stderr",
)
def test_capture_stderr_subdir(app: SphinxTestApp, ref_path: Path) -> None:
    """Test in which the file is saved inside a directory, that needs to be created."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "hello-world")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"
