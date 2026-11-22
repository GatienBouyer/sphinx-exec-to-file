"""Define the `.. exec:code::` directive."""
import sys
from pathlib import Path

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

    def make_replacements(self, paths: set[Path], command: str) -> list[str]:
        """Replace the marked paths in the command with the actual file paths.
        Return the args to execute the command with the replaced path."""
        args = command.split()
        marker_start, marker_end = self.config.exec_code_file_markers
        remaining = paths.copy()
        for i, arg in enumerate(args):
            if not arg.startswith(marker_start) or not arg.endswith(marker_end):
                continue
            for path in paths:
                path_as_arg = marker_start + path.name + marker_end
                if path_as_arg == arg:
                    break
            else:
                raise self.warning(f"'{self.name}' does not define the capture of '{arg}' "
                                   f"for the command:\n{command}")
            remaining.remove(path)
            args[i] = path.as_posix()

        for path in remaining:
            raise self.warning(f"'{self.name}' does not use '{path.name}' "
                               f"in the command:\n{command}")
        return args

    def build_command(self, args: list[str]) -> tuple[str | None, list[str]]:
        """Build the command to be executed using the mapping option."""
        exe_mapping = {
            "python": sys.executable,  # TODO test it (and make it convenient)
            "sh": None,
        }
        if self.arguments:
            language = self.arguments[0]
            if language in exe_mapping:
                exe = exe_mapping[language]
            else:
                raise self.error(f"No executable defined for language '{language}'")
        else:
            exe = None

        return exe, args

    def run(self) -> list[Node]:
        """Implementation of the directive.

        - Take the command from the content.
        - Parse the capture options
        - Replace the files that needs to be captured
        - Build the command
        - Run the command and check the output
        """
        self.assert_has_content()
        command = "\n".join(self.content)

        captures = self.get_captures()
        args = self.make_replacements(captures.paths_to_replace, command)
        exe, args = self.build_command(args)
        return list(self.exec(exe, args, captures))
