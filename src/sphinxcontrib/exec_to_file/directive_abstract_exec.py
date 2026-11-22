"""Define the common directive options and associated code to be used in 'exec' directives."""
import subprocess
from abc import ABC
from collections.abc import Iterable
from collections.abc import Sequence
from pathlib import Path
from typing import IO
from typing import NamedTuple
from typing import TypeAlias

from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
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


StdIoFd: TypeAlias = IO[str] | IO[bytes] | int | None
"""Type of what subprocess.run accepts for stdout and stderr."""


class Capture(NamedTuple):
    """Files to be captured by the directive."""
    paths_to_create: set[Path]
    paths_to_replace: set[Path]
    stdout_fd: StdIoFd
    stderr_fd: StdIoFd


class AbstractExec(SphinxDirective, ABC):
    """
    Parent class of other 'exec-*' directives.
    Store and handle the common directive options.
    """
    option_spec = {
        "capture-stdout": directives.unchanged_required,
        "capture-stderr": directives.unchanged_required,
        "capture-file": directives.unchanged_required,
        "ignore-exit": directives.flag,
        "timeout": option_positive_float,
        "hide-code": directives.flag,
    }

    @property
    def cwd(self) -> Path:
        """The directory from which the paths are constructed,
        and from where the command is run."""
        return Path(self.env.srcdir)

    def get_captures(self) -> Capture:
        """Parse the capture-file, capture-stdout, capture-sterr directive options."""
        self.env.note_reread()  # tell sphinx to re-run the directive each time
        cwd = self.cwd
        paths_to_create: set[Path] = set()
        for file in self.options.get("capture-file", "").split("\n"):
            if file.strip() == "":
                continue
            path = cwd / file
            if path in paths_to_create:
                raise self.warning(f"duplicate file '{file}' in '{self.name}' captured twice")
            paths_to_create.add(path)

        paths_to_replace = paths_to_create.copy()

        # pylint: disable=consider-using-with
        if stdout := self.options.get("capture-stdout", None):
            if (stdout_path := cwd / stdout) in paths_to_create:
                raise self.warning(f"duplicate file '{stdout}' in '{self.name}' captured twice")
            paths_to_create.add(stdout_path)
            stdout_fd = open(cwd / stdout, "wb")
        else:
            stdout_fd = None
        if stderr := self.options.get("capture-stderr", None):
            if stderr != stdout:
                if (stderr_path := cwd / stderr) in paths_to_create:
                    raise self.warning(f"duplicate file '{stderr}' in '{self.name}' captured twice")
                paths_to_create.add(stderr_path)
                stderr_fd: StdIoFd = open(cwd / stderr, "wb")
            else:
                stderr_fd = subprocess.STDOUT
        else:
            stderr_fd = None

        return Capture(
            paths_to_create=paths_to_create,
            paths_to_replace=paths_to_replace,
            stdout_fd=stdout_fd,
            stderr_fd=stderr_fd,
        )

    def make_replacements(self, paths: set[Path], srcf: Iterable[str]) -> Iterable[str]:
        """Copy and replace the marked paths by the actual file paths
        in the source file to the temporary file."""
        marker_start, marker_end = self.config.exec_code_file_markers
        remaining = paths.copy()
        for line in srcf:
            for path in paths:
                path_as_arg = marker_start + path.name + marker_end
                if path_as_arg in line:
                    remaining.discard(path)
                    line = line.replace(path_as_arg, path.as_posix())
            yield line

        for path in remaining:
            raise self.warning(f"'{self.name}' does not use '{path.name}'")

    def exec(self, exe: str | None, args: list[str], captures: Capture) -> Sequence[Node]:
        """Execute the command composed of the given args with the specifiede executable.
        Capture the stdout/stderr and check that the files are created.
        Return the directive contained nodes."""
        logged_command = " ".join(args)
        logger.info(f"Command launched: {logged_command}")
        timeout = self.options.get("timeout")

        try:
            res = subprocess.run(
                args, cwd=self.cwd, executable=exe,
                stdout=captures.stdout_fd, stderr=captures.stderr_fd,
                check=False, timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            raise self.severe(f"Timeout expired in the '{self.name}' directive "
                              f"({timeout}s) for the command:\n{logged_command}\n") from None

        if "ignore-exit" not in self.options and res.returncode != 0:
            raise self.warning(f"Command executed by the '{self.name}' directive has failed:\n"
                               f"{logged_command}\n")
        for path in captures.paths_to_create:
            if not path.exists():
                raise self.warning(f"Command executed but didn't create the file {path.name}:\n"
                                   f"{logged_command}\n")

        if "hide-code" not in self.options:
            return super().run()
        return []
