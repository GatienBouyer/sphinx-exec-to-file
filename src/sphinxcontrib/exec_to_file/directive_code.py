"""Define the `.. exec:code::` directive."""
from docutils.nodes import Node
from sphinx.directives.code import CodeBlock
from sphinx.util.logging import getLogger

from sphinxcontrib.exec_to_file.directive_abstract_exec import AbstractExec

logger = getLogger("sphinx.exec-to-file")


class ExecCodeDirective(AbstractExec, CodeBlock):
    """Define the directive that execute code."""
    name = "code"

    has_content = True
    required_arguments = 0
    optional_arguments = 1  # the language
    option_spec = {
        **CodeBlock.option_spec,
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
        self.assert_has_content()
        script_lines = self.content
        captures = self.get_captures()
        lines = self.make_replacements(captures.paths_to_replace, script_lines)
        args = self.build_command(
            self.config.exec_code_runners,
            self.arguments[0] if self.arguments else None,
            ["\n".join(lines)],
        )
        return list(self.exec(args, captures))
