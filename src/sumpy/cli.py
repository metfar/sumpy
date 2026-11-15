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
from sumui.cli import SumArgumentParser;
import os;
import runpy;
import sys;
from . import __version__;

def _run_script(filename, arguments):
    """Execute a Python file with the same import-root rules as python FILE.""";
    previous_argv = sys.argv;
    previous_path = sys.path[:];
    script_directory = os.path.dirname(os.path.abspath(filename));
    try:
        sys.argv = [filename] + list(arguments);
        sys.path.insert(0, script_directory);
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
