"""Test the execution of the code given to the exec-code directive."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

# pylint: disable=duplicate-code


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-local-script",
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
    testroot="exec-code-sys-script",
)
def test_sys_script(app: SphinxTestApp, ref_path: Path) -> None:
    """Test to exec a script that is found in the PATH env var."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-multiline-script",
)
def test_multiline_script(app: SphinxTestApp) -> None:
    """Test to exec a script that written on multiple lines."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-no-code",
)
def test_no_code(app: SphinxTestApp) -> None:
    """Test in which the code is missing form the directive content."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: ERROR: Content block expected for the \"exec:code\" directive; none found"
    assert msg in warnings
