"""Test the usage of the code-block directive to show the code of the exec-code directive."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-show-code",
)
def test_show_code(app: SphinxTestApp, ref_path: Path) -> None:
    """Test to exec a script and show the code."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table-with-command")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-lang-default",
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
    testroot="exec-code-lang-unknown",
)
def test_language_unknown(app: SphinxTestApp) -> None:
    """Test in which the language is not in the mapping."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: ERROR: No executable defined for language 'niche-language'"
    assert msg in warnings
