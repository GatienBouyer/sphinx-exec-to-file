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
    testroot="exec-code-multiline-script",
)
def test_multiline_script(app: SphinxTestApp) -> None:
    """Test to exec a script that written on multiple lines."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings


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
