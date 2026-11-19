"""Define the `.. exec:file::` directive."""
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import IO
from typing import Any

from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.directives.code import LiteralInclude
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


class ExecFileDirective(LiteralInclude):
    """Define the directive that execute code."""
    name = "file"

    has_content = False
    required_arguments = 1  # the file
    optional_arguments = 0
    option_spec = {
        **LiteralInclude.option_spec,
        "capture-stdout": directives.unchanged_required,
        "capture-stderr": directives.unchanged_required,
        "capture-file": directives.unchanged_required,
        "ignore-exit": directives.flag,
        "timeout": option_positive_float,
        "hide-code": directives.flag,
    }

    def run(self) -> list[Node]:
        """Implementation of the directive.

        - Take the command from the content.
        - Replace the files that needs to be captured
        - Run the command
        - Check the run exit code and the file creation
        """
        self.env.note_reread()

        cwd = Path(self.env.srcdir)
        file_to_exec = cwd / self.arguments[0]
        if not file_to_exec.exists():
            raise self.severe(f"Failed to found the file to execute: {file_to_exec}")

        paths_to_create: set[Path] = set()
        for file in self.options.get("capture-file", "").split("\n"):
            if file.strip() == "":
                continue
            path = Path(file)
            if path in paths_to_create:
                raise self.warning(f"duplicate file '{file}' in '{self.name}' captured twice "
                                   f"for the file:\n{file_to_exec}")
            paths_to_create.add(path)

        remaining_paths = paths_to_create.copy()

        if stdout := self.options.get("capture-stdout", None):
            if Path(stdout) in paths_to_create:
                raise self.warning(f"duplicate file '{stdout}' in '{self.name}' captured twice "
                                   f"for the file:\n{file_to_exec}")
            paths_to_create.add(Path(stdout))
            stdout_fd = open(cwd / stdout, "wb")  # pylint: disable=consider-using-with
        else:
            stdout_fd = None
        if stderr := self.options.get("capture-stderr", None):
            if stderr != stdout:
                if Path(stderr) in paths_to_create:
                    raise self.warning(f"duplicate file '{stderr}' in '{self.name}' captured twice "
                                       f"for the command:\n{file_to_exec}")
                paths_to_create.add(Path(stderr))
                # pylint: disable=consider-using-with
                stderr_fd: IO[Any] | int | None = open(cwd / stderr, "wb")
            else:
                stderr_fd = subprocess.STDOUT
        else:
            stderr_fd = None

        marker_start, marker_end = self.config.exec_code_file_markers
        with (
            open(file_to_exec, "r", encoding="utf-8") as srcf,
            tempfile.NamedTemporaryFile("w", encoding="utf-8") as tmpf,
        ):
            for line in srcf:
                for path in paths_to_create:
                    path_as_arg = marker_start + path.name + marker_end
                    if path_as_arg in line:
                        remaining_paths.discard(path)
                        replaced_line = line.replace(path_as_arg, path.as_posix())
                        tmpf.write(replaced_line)
                    else:
                        tmpf.write(line)
            tmpf.flush()

            for path in remaining_paths:
                raise self.warning(f"'{self.name}' does not use '{path.name}' "
                                   f"in the file:\n{file_to_exec}")

            exe_mapping = {
                "python": [sys.executable],  # TODO test it (and make it convenient)
                "sh": ["/bin/sh"],
            }
            language = self.options.get("language", "sh")
            if language in exe_mapping:
                exe = exe_mapping[language]
            else:
                raise self.error(f"No executable defined for language '{language}'")
            args = [*exe, tmpf.name]

            logger.info(f"Command launched: {' '.join([*exe, file_to_exec.as_posix()])}")
            timeout = self.options.get("timeout")
            try:
                res = subprocess.run(
                    args, cwd=cwd,
                    stdout=stdout_fd, stderr=stderr_fd,
                    check=False, timeout=timeout,
                )
            except subprocess.TimeoutExpired:
                raise self.severe(f"Timeout expired in the '{self.name}' directive "
                                  f"({timeout}s) for the file:\n{file_to_exec}\n") from None

        if "ignore-exit" not in self.options and res.returncode != 0:
            raise self.warning(f"Command executed by the '{self.name}' directive has failed:\n"
                               f"{file_to_exec}\n")
        for path in paths_to_create:
            if not (cwd / path).exists():
                raise self.warning(f"Command executed but didn't create the file {path.name}:\n"
                                   f"{file_to_exec}\n")

        if "hide-code" not in self.options:
            return super().run()
        return []
