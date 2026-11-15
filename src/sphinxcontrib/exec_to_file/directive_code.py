"""Define the `.. exec:code::` directive."""

from pathlib import Path

from docutils.nodes import Node
from docutils.parsers.rst.directives import flag
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.logging import getLogger

logger = getLogger("sphinx.exec-to-file")


class ExecCodeDirective(SphinxDirective):
    """Define the directive that execute code."""
    name = "code"

    has_content = True
    option_spec = {
        "capture-stdout": str,
        "capture-stderr": str,
        "capture-file": str,
        "hide-code": flag,
        "language": str,
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
        for path in paths_to_create:
            path_as_arg = "<" + path.name + ">"  # TODO add option to use other characters
            for i, arg in enumerate(args):
                if arg == path_as_arg:
                    break
            else:
                raise self.warning(
                    f"'{self.name}' doesn't use '{path_as_arg}' in the command {command}"
                )
            args[i] = path.as_posix()

        import subprocess
        import sys
        args.insert(0, sys.executable)
        logged_command = " ".join(args) 
        logger.info(f"Command launched: {logged_command}")
        res = subprocess.run(args, cwd=self.env.srcdir, check=False)
        if res.returncode != 0:  # TODO add option expected-exit-code && ignore-exit-code options
            raise self.warning(f"Command executed by the '{self.name}' directive has failed:\n"
                               f"{logged_command}\n")
        for path in paths_to_create:
            if not path.exists():
                raise self.warning(f"Command executed but didn't create the file {path.name}:\n"
                                   f"{logged_command}\n") 
        return []
