"""Test the execution of the code given to the extension directives."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp

# pylint: disable=duplicate-code


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-script-failure",
)
def test_script_failure(app: SphinxTestApp) -> None:
    """Test in which the script called failed with an exit code != 0."""
    app.build()
    warnings = app.warning.getvalue()
    msg = "index.rst:1: WARNING: Command executed by the 'exec:code' directive has failed:"
    assert msg in warnings


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-script-failure-ignored",
)
def test_script_failure_ignore(app: SphinxTestApp, ref_path: Path) -> None:
    """Test in which the option ignore-exit is used to avoid the warning on the exit code != 0."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    diff = dircmp(output := app.outdir, ref := ref_path / "csv-table")
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"


@pytest.mark.sphinx(
    buildername="text",
    testroot="exec-code-timeout",
)
def test_timeout(app: SphinxTestApp) -> None:
    """Test in which the code doesn't finished and reach the defined timeout."""
    app.build()
    warnings = app.warning.getvalue()
    msg = ("index.rst:1: CRITICAL: Timeout expired in the 'exec:code' directive (0.1s) "
           "for the command:\nlocal_prog.py")
    assert msg in warnings
