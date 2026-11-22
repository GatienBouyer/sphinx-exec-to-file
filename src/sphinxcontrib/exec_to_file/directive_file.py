"""Define the `.. exec:file::` directive."""
import tempfile

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

            args = self.build_command(
                self.config.exec_file_runners,
                self.options.get("language"),
                [tmpf.name],
            )
            return list(self.exec(args, captures))
