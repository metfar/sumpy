# SUM CLI migration — sumpy 0.1.0a14

The command-line entry points in this local development snapshot adopt the
`sumui.cli.SumArgumentParser` contract where appropriate, retaining historical
arguments and specialized behavior. The `sumcore` package is the architectural
exception: its own executable uses `sys.argv` and its auxiliary programs stay
independent of `sumUI`.

This is a **local development build**, not a published release. Verify normal
runtime behavior in the target environment before promoting to the repository.

## Source-path compatibility fix

The `sumpy` and `sumPY` frontends continue to use `SumArgumentParser`.
When executing a Python file, they temporarily prepend the source directory to
`sys.path`, forward all arguments after the filename unchanged, and restore
`sys.argv` and `sys.path` on return or exception. This matches the practical
import behavior of `python script.py` for sibling modules.

The original failure was reproduced with `demo_hexview.py` from `ver1.2`: its
`from _demo_catalog import run` failed because the wrapper resided in another
directory. `sumpy demo_hexview.py --snapshot` now completes successfully under
a non-interactive integration test.

The patch affects only `sumpy`. No change to `sumUI`, `sumTUI`, or the example
source is required.

<p align=center><b>- oOo -</b></p>
