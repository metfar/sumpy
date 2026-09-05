# sumpy

Python runtime facade for the Sum ecosystem.


## r20.1 graphical acceptance example

The equivalent SUM Python route uses the same `sumPlot` semantics and renderer:

```bash
sumpy examples/mtcars_mpg_density_blue.py
```

It writes `mtcars_mpg_density_blue_sumpy.png`; for the reference histogram this output is generated from the same resolved plot as sumR.

<p align=center><b>- oOo -</b></p>

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
from sumpy import beep, play, sound, stop_audio;

beep(.25, 12);
sound(440, 18.2);
play("T180O5cdefgabC");
stop_audio();
```

These are thin adapters over `sumcore.audio`; sumPY does not maintain a second
synthesizer.

<p align=center><b>- oOo -</b></p>
