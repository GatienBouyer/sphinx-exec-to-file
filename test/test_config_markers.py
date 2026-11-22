"""Test the exec_code_file_markers extension configuration option."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

# pylint: disable=duplicate-code


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-config-marker-chars",
)
def test_config_marker_chars_tuple(app: SphinxTestApp, ref_path: Path) -> None:
    """Test in which the exec_code_file_markers config option is used with '("{", "}")'."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-config-marker-chars",
    confoverrides={"exec_code_file_markers": "{}"},
)
def test_config_marker_chars_string(app: SphinxTestApp, ref_path: Path) -> None:
    """Test in which the exec_code_file_markers config option is used with '{}'."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-config-marker-chars",
    confoverrides={"exec_code_file_markers": "-"}
)
def test_config_marker_chars_invalid(app: SphinxTestApp) -> None:
    """Test in which the exec_code_file_markers config option is used with an invalid value."""
    with pytest.raises(ValueError):
        app.build()
