"""Test the extension."""
from filecmp import dircmp
from pathlib import Path

import pytest
from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx(
    buildername="text",
    testroot="nominal",
)
def test_nominal(app: SphinxTestApp, ref_path: Path) -> None:
    """Test a default build."""
    app.build()
    warnings = app.warning.getvalue()
    assert not warnings
    output = app.outdir
    ref = ref_path / "nominal"
    diff = dircmp(output, ref)
    assert not (diff.diff_files or diff.left_only or diff.right_only), f"{output} != {ref}"
