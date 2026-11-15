# sumpy

Python runtime facade for the Sum ecosystem.


## r20.1 graphical acceptance example

The equivalent SUM Python route uses the same `sumPlot` semantics and renderer:

```bash
sumpy examples/mtcars_mpg_density_blue.py
```

It writes `mtcars_mpg_density_blue_sumpy.png`; for the reference histogram this output is generated from the same resolved plot as sumR.

## Graphical acceptance example

`examples/mtcars_mpg_density_blue.py` builds the same density histogram as the sumR example, renders it, saves a PNG and opens it through `xdg-open` without blocking.


## r20.1 graphical acceptance example

The equivalent SUM Python route uses the same `sumPlot` semantics and renderer:

```bash
sumpy examples/mtcars_mpg_density_blue.py
```

It writes `mtcars_mpg_density_blue_sumpy.png`; for the reference histogram this output is generated from the same resolved plot as sumR.

## Shared audio

```python
from sumpy import beep, midi_frequency, play, sound, stop_audio, tone_wav_bytes;

beep(.25, 12);
sound(440, 18.2);
play("T180O5cdefgabC");

a4 = midi_frequency(69);
wav = tone_wav_bytes(a4, .25, volume=.4);
stop_audio();
```

These are thin adapters over `sumcore.audio`; sumPY does not maintain a second
synthesizer.


Audio examples: `examples/audio.py` demonstrates `beep()`, `sound()` and `play()` through the shared `sumcore` service. `examples/piano.py` keeps the original Pygame polyphonic keyboard/ADSR model but sources each note from the canonical Sum/BASIC generator through SumGUI.

## Shared helpers

`sumpy` exposes the common sum text/format helpers directly: `repeat`, `mid`, `instr`, `trim`, `like`, `ilike`, `numformat`, `dateformat`, `textformat` and `boolformat`. String positions are zero-based.

```python
repeat("ab",3)
mid("abcdef",0,1)
instr("abcdef","cd")
numformat(5,"$ 0000.00")
boolformat(None,"NO|SI|OMITIDO")
```

## CLI execution parity — 0.1.0a15

`sumPY`/`sumpy` execute a Python script with its own directory at the front of
`sys.path`, as `python script.py` does. This allows imports of sibling modules
(e.g., `from _demo_catalog import run`) even when the command was installed as
a console entry point in `~/.local/bin`. The current working directory remains
unchanged. The caller's `sys.argv` and `sys.path` are restored if the interpreter
returns or the executed script raises an exception.

```bash
cd sumtui/examples
sumpy demo_hexview.py --snapshot
sumpy demo_hexview.py --help
sumpy --version
sumpy -c 'print("SUM")'
```

Options **after** the script filename are passed to the script without being
processed by the launcher, including `--help`, `--version`, and theme switches.
Options **before** the filename belong to the common SUM CLI parser. `-c`
executes inline Python and makes the current directory importable.

This is a local fix for the source-path/import issue in 0.1.0a12; it does not
change `sumUI`, `sumTUI` or the examples.

## Selective pygame startup warnings — 0.1.0a15

When running scripts via `sumpy`, only these two known Pygame import notices
are suppressed by default:

- `RuntimeWarning: Your system is avx2 capable but pygame was not built with support for it`
- `UserWarning: pkg_resources is deprecated as an API` attributed to `pygame.pkgdata`

All other warnings and all exceptions remain visible. Warning filters are in
force only during `sumpy FILE.py` and `sumpy -c '...'`, and are restored at exit.
For diagnostics, restore those two warnings without changing dependencies:

```bash
SUMPY_SHOW_PYGAME_WARNINGS=1 sumpy demo_bgi_compat.py
```

This is a warning-display policy, not an AVX2 optimization or a removal of
`pkg_resources`. The latter belongs to the installed Pygame package, not SUM;
its future compatibility depends on that package's resource-loading fallback.

## Educational diagnostics — 0.1.0a15

SUM interpreters prioritize the information needed for the lesson. Known,
non-actionable third-party startup warnings may be hidden during normal
execution, **without hiding Python exceptions, errors, or unrelated warnings**.
The current `sumpy` implementation only filters Pygame's AVX2 build notice
and the `pkg_resources` deprecation reported by `pygame.pkgdata`.

For lessons and normal execution:

```bash
sumpy demo_bgi_compat.py
```

For maintenance or teaching the internals, explicitly request all warnings:

```bash
sumpy --full-debug demo_bgi_compat.py
sumpy --fullDebug demo_bgi_compat.py
sumpy --full-debug -c 'import warnings; warnings.warn("example")'
```

The option belongs to the interpreter **before** `FILE` or `-c`.
Arguments after the script's filename are passed to that script unchanged:

```bash
sumpy demo_bgi_compat.py --full-debug  # belongs to the example, not sumpy
```

The legacy `SUMPY_SHOW_PYGAME_WARNINGS=1` environment switch still works.
`--full-debug` additionally requests `warnings.simplefilter("always")` during
script execution. Warning-filter state is restored afterward. Python exceptions
retain their normal full tracebacks in both modes; this is not a catch-all
error suppression mechanism and does not forcibly enable unrelated loggers.

**Scope:** invoking the same file through `python demo.py` bypasses this
interpreter and its filter. Other SUM interpreters can implement this same
contract independently; they are not changed by this sumPY release.

<p align=center><b>- oOo -</b></p>
