"""Test the extension."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp


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
    testroot="exec-code-capture-multiple-files",
)
def test_capture_multipe_files(app: SphinxTestApp, ref_path: Path) -> None:
    """Test in which the script called generated multiple files."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table-multiple")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-show-code",
)
def test_show_code(app: SphinxTestApp, ref_path: Path) -> None:
    """Test to exec a script and show the code."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table-with-code")
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


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-no-code",
)
def test_no_code(app: SphinxTestApp) -> None:
    """Test in which the code is missing form the directive content."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: WARNING: Content expected for the 'exec:code' directive; 0 found"
    assert msg in warnings


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-script-failure",
)
def test_script_failure(app: SphinxTestApp) -> None:
    """Test in which the script called failed with an exit code != 0."""
    app.build()
    warnings = app.warning.getvalue()
    msg = ("index.rst:1: WARNING: Command executed by the 'exec:code' directive has failed:\n"
           "local_prog.py data.csv")
    assert msg in warnings


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-file-not-created",
)
def test_file_not_created(app: SphinxTestApp) -> None:
    """Test in which the script called does not create the captured file."""
    app.build()
    warnings = app.warning.getvalue()
    msg = ("index.rst:1: WARNING: Command executed but didn't create the file data.csv:\n"
           "local_prog.py data.csv")
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
