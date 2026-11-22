"""Define the `.. exec:file::` directive."""
import sys
import tempfile
from typing import IO

from docutils.nodes import Node
from sphinx.directives.code import LiteralInclude
from sphinx.util.logging import getLogger

from sphinxcontrib.exec_to_file.directive_abstract_exec import AbstractExec

logger = getLogger("sphinx.exec-to-file")


class ExecFileDirective(AbstractExec, LiteralInclude):
    """Define the directive that execute code."""
    name = "file"

    has_content = False
    required_arguments = 1  # the file
    optional_arguments = 0
    option_spec = {
        **LiteralInclude.option_spec,
        **AbstractExec.option_spec,
    }

    def build_command(self, tmpf: IO[str]) -> tuple[str | None, list[str]]:
        """Build the command to be executed using the mapping option."""
        exe_mapping = {
            "python": [sys.executable],
            "sh": ["/bin/sh"],
        }
        language = self.options.get("language", "sh")
        if language in exe_mapping:
            exe = exe_mapping[language]
        else:
            raise self.error(f"No executable defined for language '{language}'")
        return None, [*exe, tmpf.name]

    def run(self) -> list[Node]:
        """Implementation of the directive.

        - Take the command from the content.
        - Parse the capture options
        - Replace the files that needs to be captured
        - Build the command
        - Run the command and check the output
        """
        file_to_exec = self.cwd / self.arguments[0]
        if not file_to_exec.exists():
            raise self.severe(f"Failed to found the file to execute: {file_to_exec}")

        captures = self.get_captures()
        with (
            open(file_to_exec, "r", encoding="utf-8") as srcf,
            tempfile.NamedTemporaryFile("w", encoding="utf-8") as tmpf,
        ):
            for line in self.make_replacements(captures.paths_to_replace, srcf):
                tmpf.write(line)
            tmpf.flush()
            exe, args = self.build_command(tmpf)
            return list(self.exec(exe, args, captures))
