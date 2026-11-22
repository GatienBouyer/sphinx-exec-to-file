"""Test the usage of the literalinclude directive to show the code of the exec-file directive."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-show-code",
)
def test_show_code(app: SphinxTestApp, ref_path: Path) -> None:
    """Test to exec a script file and show the code."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table-with-code")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-lang-default",
)
def test_language_default(app: SphinxTestApp, ref_path: Path) -> None:
    """Test in which the language is not set."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-file-lang-unknown",
)
def test_language_unknown(app: SphinxTestApp) -> None:
    """Test in which the language is not in the mapping."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: ERROR: No executable defined for language 'niche-language'"
    assert msg in warnings
