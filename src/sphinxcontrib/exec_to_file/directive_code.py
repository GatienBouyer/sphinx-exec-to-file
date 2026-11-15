"""Define the `.. exec:code::` directive."""

from pathlib import Path

from docutils.nodes import Node
from docutils.parsers.rst.directives import flag
from sphinx.application import Sphinx
from sphinx.directives.code import CodeBlock
from sphinx.util.logging import getLogger

logger = getLogger("sphinx.exec-to-file")


class ExecCodeDirective(CodeBlock):
    """Define the directive that execute code."""
    name = "code"

    has_content = True
    optional_arguments = 1  # the language
    option_spec = {
        **CodeBlock.option_spec,
        "capture-stdout": str,
        "capture-stderr": str,
        "capture-file": str,
        "hide-code": flag,
    }

    @classmethod
    def register(cls, app: Sphinx, domain_name: str) -> None:
        """Register the directive in the Sphinx registry."""
        app.add_directive_to_domain(domain_name, cls.name, cls)
        # app.add_config_value("") TODO

    def run(self) -> list[Node]:
        """Implementation of the directive.

        - Take the command from the content.
        - Replace the files that needs to be captured
        - Run the command
        - Check the run exit code and the file creation
        """
        if len(self.content) != 1:
            raise self.warning(
                f"Content expected for the '{self.name}' directive; {len(self.content)} found"
            )
        command = self.content[0]

        args = command.split()
        # TODO check for missing option values and duplicate file name
        files_to_create = set(self.options.get("capture-file", "").split("\n"))
        files_to_create.discard("")

        paths_to_create = {Path(f) for f in files_to_create}
        remaining_paths = paths_to_create.copy()
        for i, arg in enumerate(args):
            # TODO add option to use other characters
            if not arg.startswith("<") or not arg.endswith(">"):
                continue
            for path in paths_to_create:
                path_as_arg = "<" + path.name + ">"
                if path_as_arg == arg:
                    break
            else:
                raise self.warning(f"'{self.name}' does not define the capture of '{arg}' "
                                   f"for the command:\n{command}")
            args[i] = path.as_posix()
            remaining_paths.remove(path)

        for path in remaining_paths:
            raise self.warning(f"'{self.name}' does not use '{path.name}' "
                               f"in the command:\n{command}")

        import subprocess
        import sys
        exe_mapping = {
            "python": sys.executable,
            "sh": None,
        }
        if self.arguments:
            language = self.arguments[0]
            if language in exe_mapping:
                exe = exe_mapping[self.arguments[0]]
            else:
                raise self.error(f"No executable defined for language '{language}'")
        else:
            exe = None

        logged_command = " ".join(args)
        logger.info(f"Command launched: {logged_command}")
        cwd = Path(self.env.srcdir)
        res = subprocess.run(args, cwd=cwd, executable=exe, check=False)

        if res.returncode != 0:  # TODO add option ignore-exit-code
            raise self.warning(f"Command executed by the '{self.name}' directive has failed:\n"
                               f"{logged_command}\n")
        for path in paths_to_create:
            if not (cwd / path.name).exists():
                raise self.warning(f"Command executed but didn't create the file {path.name}:\n"
                                   f"{logged_command}\n")

        if "hide-code" not in self.options:
            return super().run()
        return []
