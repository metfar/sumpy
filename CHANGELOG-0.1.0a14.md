# sumPY 0.1.0a14 — Selective Pygame warning policy

- Ignore only Pygame's AVX2 build warning and the `pkg_resources` deprecation
  attributed to `pygame.pkgdata` during script execution.
- Do not affect unrelated warnings, exceptions, or parent-process filters.
- Opt-in diagnostic mode: `SUMPY_SHOW_PYGAME_WARNINGS=1`.
- Applies consistently to `sumpy FILE` and `sumpy -c`.
- Do not modify Pygame or suppress all Python warnings.

<p align=center><b>- oOo -</b></p>
