# sumPY 0.1.0a14 — CLI script-import compatibility

**Origin:** User report on 2026-11-15 while running
`sumtui/examples/demo_hexview.py` with `sumpy`.

## Root cause

The console-script entry point `~/.local/bin/sumpy` called `runpy.run_path()`
with an unchanged `sys.path`. Unlike `python demo_hexview.py`, it did not insert
`demo_hexview.py`'s directory, so local `_demo_catalog.py` was not importable.

## Implemented

- Temporarily insert the script directory at the start of `sys.path`.
- Forward all arguments after the script filename, including `--help`,
  `--version` and theme flags, without parsing them as launcher options.
- Preserve and restore the caller's `sys.argv` and `sys.path`, including when
  the script raises an exception.
- Make the working directory importable in inline `-c` mode.
- Increment package and runtime version from 0.1.0a12 to 0.1.0a14.
- Preserve the existing `SumArgumentParser` and SUM theme functionality.

## Tests

- 9 targeted tests passed using the real sumUI parser and a minimal sumPY
  package stub to avoid optional plotting/audio dependencies.
- The unchanged `demo_hexview.py` from `ver1.2.zip` completed successfully
  with `--snapshot`: exit code 0, 3029 bytes stdout, empty stderr.
- Python syntax compilation passed.
- Wheel `sumpy-0.1.0a14-py3-none-any.whl` built successfully.

## Not tested

- A live terminal/TUI session under Python 3.14 on the user's machine.
- All the other SUM applications and their dependency combinations.

No source repository or online service was modified.

<p align=center><b>- oOo -</b></p>
