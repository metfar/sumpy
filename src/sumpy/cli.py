#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#pylint:disable=W0301
#  
#  Copyright 2018- William Martinez Bas <metfar@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
import argparse;
from contextlib import contextmanager;
import warnings;
from sumui.cli import SumArgumentParser;
import os;
import runpy;
import sys;
from . import __version__;


@contextmanager
def _pygame_warnings():
    """Hide only two known Pygame startup notices, never other warnings.

    The filters are scoped to executed code, leaving the embedding process's
    warning configuration unchanged. Use SUMPY_SHOW_PYGAME_WARNINGS=1 to inspect
    both warnings without changing the application or system packages.
    """;
    if str(os.environ.get("SUMPY_SHOW_PYGAME_WARNINGS", "")).strip().casefold() in ("1", "yes", "true", "on"):
        yield;
        return;
    with warnings.catch_warnings():
        # Pygame's compiled blitter warning may be attributed to importlib.
        warnings.filterwarnings(
            "ignore",
            message=r"^Your system is avx2 capable but pygame was not built with support for it\.",
            category=RuntimeWarning,
        );
        # Stacklevel attributes this deprecation to pygame.pkgdata:25.
        warnings.filterwarnings(
            "ignore",
            message=r"^pkg_resources is deprecated as an API\.",
            category=UserWarning,
            module=r"^pygame\.pkgdata$",
        );
        yield;


def _run_script(filename, arguments):
    """Execute a Python file with the same import-root rules as python FILE.""";
    previous_argv = sys.argv;
    previous_path = sys.path[:];
    script_directory = os.path.dirname(os.path.abspath(filename));
    try:
        sys.argv = [filename] + list(arguments);
        sys.path.insert(0, script_directory);
        with _pygame_warnings():
            runpy.run_path(filename, run_name="__main__");
        return 0;
    finally:
        sys.argv = previous_argv;
        sys.path[:] = previous_path;


def _run_command(command, arguments):
    """Execute -c with the current working directory available for imports.""";
    previous_argv = sys.argv;
    previous_path = sys.path[:];
    try:
        sys.argv = ["-c"] + list(arguments);
        sys.path.insert(0, "");
        with _pygame_warnings():
            exec(compile(command, "<string>", "exec"), {"__name__": "__main__", "__package__": None, "__spec__": None});
        return 0;
    finally:
        sys.argv = previous_argv;
        sys.path[:] = previous_path;


def main(argv=None):
    parser = SumArgumentParser(prog="sumPY", description="SUM Python runtime facade.");
    parser.add_argument("--version", action="version", version="sumPY {}".format(__version__));
    parser.add_argument("-c", "--command", help="execute Python source provided as a string");
    parser.add_argument("file", nargs="?", help="Python source file to execute");
    # After FILE all arguments belong to the script, including -h/--help,
    # --version and flags whose names also exist in the SUM CLI.
    parser.add_argument("script_args", nargs=argparse.REMAINDER, metavar="ARG");
    args, unknown = parser.parse_known_args(argv);
    if args.command is not None:
        tail = list(unknown);
        if args.file is not None:
            tail.append(args.file);
        tail.extend(args.script_args);
        return _run_command(args.command, tail);
    if not args.file:
        parser.print_help();
        return 0;
    return _run_script(args.file, list(unknown) + args.script_args);


if __name__ == "__main__":
    raise SystemExit(main());
