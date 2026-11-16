"""Define the `.. exec:code::` directive."""
import subprocess
import sys
from pathlib import Path
from typing import IO
from typing import Any

from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.directives.code import CodeBlock
from sphinx.util.logging import getLogger

logger = getLogger("sphinx.exec-to-file")


def option_positive_float(argument: str) -> float:
    """
    Converts the argument into a float.  Raises ValueError for negative,
    zero, or non-integer values.  (Directive option conversion function.)
    """
    value = float(argument)
    if value <= 0:  # pragma: no cover
        raise ValueError('negative or zero value; must be positive')
    return value


class ExecCodeDirective(CodeBlock):
    """Define the directive that execute code."""
    name = "code"

    has_content = True
    optional_arguments = 1  # the language
    option_spec = {
        **CodeBlock.option_spec,
        "capture-stdout": directives.unchanged_required,
        "capture-stderr": directives.unchanged_required,
        "capture-file": directives.unchanged_required,
        "ignore-exit": directives.flag,
        "timeout": option_positive_float,
        "hide-code": directives.flag,
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
        self.env.note_reread()

        command = self.content[0]
        args = command.split()
        cwd = Path(self.env.srcdir)

        paths_to_create: set[Path] = set()
        for file in self.options.get("capture-file", "").split("\n"):
            if file.strip() == "":
                continue
            path = Path(file)
            if path in paths_to_create:
                raise self.warning(f"duplicate file '{file}' in '{self.name}' captured twice "
                                   f"for the command:\n{command}")
            paths_to_create.add(path)

        if stdout := self.options.get("capture-stdout", None):
            if Path(stdout) in paths_to_create:
                raise self.warning(f"duplicate file '{stdout}' in '{self.name}' captured twice "
                                   f"for the command:\n{command}")
            paths_to_create.add(Path(stdout))
            stdout_fd = open(cwd / stdout, "wb")  # pylint: disable=consider-using-with
        else:
            stdout_fd = None
        if stderr := self.options.get("capture-stderr", None):
            if stderr != stdout:
                if Path(stderr) in paths_to_create:
                    raise self.warning(f"duplicate file '{stderr}' in '{self.name}' captured twice "
                                       f"for the command:\n{command}")
                paths_to_create.add(Path(stderr))
                # pylint: disable=consider-using-with
                stderr_fd: IO[Any] | int | None = open(cwd / stderr, "wb")
            else:
                stderr_fd = subprocess.STDOUT
        else:
            stderr_fd = None

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

        exe_mapping = {
            "python": sys.executable,  # TODO test it (and make it convenient)
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
        timeout = self.options.get("timeout")
        try:
            res = subprocess.run(
                args, cwd=cwd, executable=exe,
                stdout=stdout_fd, stderr=stderr_fd,
                check=False, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            raise self.severe(f"Timeout expired in the '{self.name}' directive "
                              f"({timeout}s) for the command:\n{command}\n") from None

        if "ignore-exit" not in self.options and res.returncode != 0:
            raise self.warning(f"Command executed by the '{self.name}' directive has failed:\n"
                               f"{logged_command}\n")
        for path in paths_to_create:
            if not (cwd / path).exists():
                raise self.warning(f"Command executed but didn't create the file {path.name}:\n"
                                   f"{logged_command}\n")

        if "hide-code" not in self.options:
            return super().run()
        return []
