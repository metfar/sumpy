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

<p align=center><b>- oOo -</b></p>

Audio examples: `examples/audio.py` demonstrates `beep()`, `sound()` and `play()` through the shared `sumcore` service. `examples/piano.py` keeps the original Pygame polyphonic keyboard/ADSR model but sources each note from the canonical Sum/BASIC generator through SumGUI.

<p align=center><b>- oOo -</b></p>
