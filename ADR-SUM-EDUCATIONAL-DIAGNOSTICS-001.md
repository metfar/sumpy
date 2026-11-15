# ADR-SUM-EDUCATIONAL-DIAGNOSTICS-001

**Status:** adopted for the sumPY launcher; design convention for other SUM
interpreters, not yet implemented in their packages.

## Motivation

Students may encounter third-party startup warnings for dependencies that
predate the course or are outside its learning objectives. Those messages can
be confused with student errors and distract from the lesson. The diagnostics
must be available to instructors and maintainers without obliging beginners to
interpret dependency internals.

## Convention

- Normal execution: show errors, exception tracebacks and meaningful warnings.
  Filter only narrowly identified, non-actionable dependency startup notices.
- Diagnostic execution: `--full-debug` and `--fullDebug` expose the complete
  Python warnings stream for the interpreted program. Future interpreters can
  expose their own additional diagnostic channels through the same switch.
- Do not hide arbitrary warnings, change third-party library files, or suppress
  exceptions. Keep the filter scope and the explicit diagnostic state local.
- Options before a script name belong to the interpreter, while options after
  its name belong to the user's script.
- No dependency on Python `argparse` inside sumCore; the command-line
  presentation convention belongs to sumUI/its interpreter clients.
- This ADR does not assert that other SUM interpreters already support the
  flag; each requires implementation and tests in its own package.
- Direct `python script.py` bypasses the SUM interpreter and therefore does
  not inherit its output policy.

## Future extensions

An optional SUM-wide diagnostics service may centralize warning IDs,
message-to-severity mapping and diagnostic sinks, while keeping the normal
educational interface quiet. This is **proposed**, not implemented.

<p align=center><b>- oOo -</b></p>
