# RUL-231: Detectors that depend on each other

Detectors are starting to build on each other's results, and we've had wrong verdicts when one runs
before the thing it depends on. Make this safe.
