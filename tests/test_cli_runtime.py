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
import json;
import os;
from pathlib import Path;
import shutil;
import subprocess;
import sys;

import pytest;


@pytest.fixture
def runtime(tmp_path):
    """Test the actual CLI without loading sumpy's optional plot libraries.""";
    root = tmp_path / "isolated-runtime";
    package = root / "sumpy";
    package.mkdir(parents=True);
    source = Path(__file__).resolve().parents[1] / "src" / "sumpy" / "cli.py";
    shutil.copy2(source, package / "cli.py");
    (package / "__init__.py").write_text('__version__ = "0.1.0a14";\n', encoding="utf-8");
    working = tmp_path / "other-directory";
    working.mkdir();
    examples = tmp_path / "project" / "examples";
    examples.mkdir(parents=True);
    (examples / "_demo_catalog.py").write_text('VALUE = "sibling-import-ok";\n', encoding="utf-8");
    (examples / "demo_hexview.py").write_text(
        'import json;\nimport os;\nimport sys;\nfrom _demo_catalog import VALUE;\n'
        'print(json.dumps({"value": VALUE, "argv": sys.argv, "path0": sys.path[0], "cwd": os.getcwd()}));\n',
        encoding="utf-8",
    );
    env = os.environ.copy();
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "");
    return {"working": working, "examples": examples, "env": env};


def execute(runtime, *args):
    return subprocess.run(
        [sys.executable, "-c", "from sumpy.cli import main; raise SystemExit(main());", *args],
        cwd=runtime["working"], env=runtime["env"], text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15, check=False,
    );


def test_local_helper_import_from_other_working_directory(runtime):
    script = runtime["examples"] / "demo_hexview.py";
    result = execute(runtime, str(script), "--snapshot", "test");
    assert result.returncode == 0, result.stderr;
    data = json.loads(result.stdout.strip());
    assert data["value"] == "sibling-import-ok";
    assert data["argv"] == [str(script), "--snapshot", "test"];
    assert data["path0"] == str(runtime["examples"].resolve());
    assert data["cwd"] == str(runtime["working"]);


@pytest.mark.parametrize("options", [["--help"], ["--version"], ["--set-theme", "ZX"], ["--get-theme"]])
def test_script_options_are_not_consumed_by_launcher(runtime, options):
    script = runtime["examples"] / "demo_hexview.py";
    result = execute(runtime, str(script), *options);
    assert result.returncode == 0, result.stderr;
    data = json.loads(result.stdout.strip());
    assert data["argv"][1:] == options;


def test_launcher_version_remains_available(runtime):
    result = execute(runtime, "--version");
    assert result.returncode == 0;
    assert result.stdout.strip() == "sumPY 0.1.0a14";


def test_run_command_imports_from_current_directory(runtime):
    (runtime["working"] / "helper.py").write_text('answer = 42;\n', encoding="utf-8");
    result = execute(runtime, "-c", 'import helper; print(helper.answer);', "extra");
    assert result.returncode == 0, result.stderr;
    assert result.stdout.strip() == "42";


def test_system_exit_code_propagates(runtime):
    script = runtime["examples"] / "exit.py";
    script.write_text('raise SystemExit(7);\n', encoding="utf-8");
    result = execute(runtime, str(script));
    assert result.returncode == 7;


def test_import_path_and_argv_are_restored_on_exception(runtime):
    script = runtime["examples"] / "exit.py";
    script.write_text('raise ValueError("deliberate");\n', encoding="utf-8");
    code = (
        "import json, sys; from sumpy.cli import main; "
        "before=(sys.argv, list(sys.path)); "
        "\ntry: main([sys.argv[-1]]); "
        "\nexcept ValueError: pass; "
        "\nprint(json.dumps([sys.argv==before[0], sys.path==before[1]]));"
    );
    proc = subprocess.run([sys.executable, "-c", code, str(script)],
        cwd=runtime["working"], env=runtime["env"], text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=15, check=False);
    assert proc.returncode == 0, proc.stderr;
    assert json.loads(proc.stdout.strip()) == [True, True];


def _make_pygame_notice_script(runtime, target):
    """Use a fake pygame.pkgdata to test policy without installing pygame.""";
    examples = runtime["examples"];
    package = examples / "pygame";
    package.mkdir(exist_ok=True);
    (package / "__init__.py").write_text("", encoding="utf-8");
    (package / "pkgdata.py").write_text(
        'import warnings;\n'
        'warnings.warn("pkg_resources is deprecated as an API. See the setuptools docs", UserWarning);\n',
        encoding="utf-8",
    );
    target.write_text(
        'import warnings;\n'
        'import pygame.pkgdata;\n'
        'warnings.warn("Your system is avx2 capable but pygame was not built with support for it. Blits may be slow", RuntimeWarning);\n'
        'warnings.warn("unrelated warning must remain visible", UserWarning);\n'
        'warnings.warn("pkg_resources is deprecated as an API. From another module", UserWarning);\n'
        'print("DONE");\n',
        encoding="utf-8",
    );


def test_pygame_notices_are_selectively_suppressed(runtime):
    script = runtime["examples"] / "pygame_warnings.py";
    _make_pygame_notice_script(runtime, script);
    proc = execute(runtime, str(script));
    assert proc.returncode == 0, proc.stderr;
    assert proc.stdout.strip() == "DONE";
    assert "Your system is avx2 capable" not in proc.stderr;
    assert "pygame/pkgdata.py" not in proc.stderr;
    assert "unrelated warning must remain visible" in proc.stderr;
    assert "From another module" in proc.stderr;


def test_pygame_notice_opt_in_reenables_both(runtime):
    script = runtime["examples"] / "pygame_warnings.py";
    _make_pygame_notice_script(runtime, script);
    runtime["env"]["SUMPY_SHOW_PYGAME_WARNINGS"] = "1";
    proc = execute(runtime, str(script));
    assert proc.returncode == 0, proc.stderr;
    assert "Your system is avx2 capable" in proc.stderr;
    assert "pkg_resources is deprecated as an API" in proc.stderr;
    assert "unrelated warning must remain visible" in proc.stderr;


def test_pygame_notices_are_suppressed_for_inline_command(runtime):
    code = ('import warnings; '
        'warnings.warn("Your system is avx2 capable but pygame was not built with support for it.", RuntimeWarning); '
        'warnings.warn("please check disk", UserWarning);');
    proc = execute(runtime, "-c", code);
    assert proc.returncode == 0, proc.stderr;
    assert "Your system is avx2 capable" not in proc.stderr;
    assert "please check disk" in proc.stderr;


def test_filter_does_not_hide_exceptions(runtime):
    script = runtime["examples"] / "raises.py";
    script.write_text('raise RuntimeError("this must not be hidden");\n', encoding="utf-8");
    proc = execute(runtime, str(script));
    assert proc.returncode != 0;
    assert "this must not be hidden" in proc.stderr;
