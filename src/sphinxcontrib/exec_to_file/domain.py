"""
Define the Sphinx domain that regroup all the features of the exec-to-file extension.
"""
from collections.abc import Iterable
from typing import Any

from docutils.nodes import Element
from docutils.nodes import reference
from sphinx.addnodes import pending_xref
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.domains import Domain
from sphinx.environment import BuildEnvironment
from sphinx.util.logging import getLogger

from sphinxcontrib.exec_to_file.directive_code import ExecCodeDirective

logger = getLogger("sphinx.exec-to-file")


class ExecToFileDomain(Domain):
    """Domain that regroup all the features of the exec-to-file extension."""
    name = "exec"
    """Name of the domain, i.e. the directive and role prefix."""
    data_version = 0
    """Version of the format of the data attribute cached by Sphinx."""

    @classmethod
    def register(cls, app: Sphinx) -> None:
        """Register the domain and its dependencies in the Sphinx registry."""
        app.add_domain(cls)
        ExecCodeDirective.register(app, cls.name)

    def merge_domaindata(self, docnames: Iterable[str], otherdata: dict[str, Any]) -> None:
        """Merge domain data of multiple document coming from different subprocesses.
        Used in Sphinx parallel builds."""

    def resolve_any_xref(
        self, env: BuildEnvironment, fromdocname: str, builder: Builder,
        target: str, node: pending_xref, contnode: Element
    ) -> list[tuple[str, reference]]:
        """Resolve the pending_xref *node* with the given *target* from the :any: role"""
        raise NotImplementedError
