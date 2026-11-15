# sumPY 0.1.0a15 — Optional complete warnings for education

- New interpreter aliases `--full-debug` and `--fullDebug`.
- Normal student mode retains selective suppression of the two known Pygame
  startup warnings without hiding unrelated warnings or failures.
- Full-debug mode shows all Python warnings emitted during the script execution.
- Preserve `SUMPY_SHOW_PYGAME_WARNINGS=1` from 0.1.0a14.
- Keep script arguments intact and preserve `sys.argv` / `sys.path` restoration.
- Scope warning configuration to the executing script, restore it afterward.
- `python script.py` is outside the `sumpy` launcher and is not modified.

<p align=center><b>- oOo -</b></p>
