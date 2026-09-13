# Traces are pulled into a file the repo owns

Anki holds the review history, and it is the only thing that does. The
obvious way to use it is for the Brief, the Feed and anything else that
needs to know how well a topic is held to ask AnkiConnect at the moment
they need it. We do not. `trellis pull` asks Anki once, writes
`traces/<domain>.json`, and stops; every other command reads that file
and has never heard of AnkiConnect.

The cost is staleness — a Brief can be built on Traces from last week,
so it says how old they are. Everything else is upside, and it is the
kind of upside that decides whether a feature gets used:

- **The loop works where Anki is not.** The Brief regenerates on a phone
  that cloned the repo, in CI, and on a laptop with Anki closed. A
  feedback loop that requires launching a desktop app is a feedback loop
  you run once.
- **The seam is a file, so it is testable.** `assess()` is a pure
  function of (skeleton, cards, traces) and its tests read a fixture, not
  a mock HTTP server. Everything hard about the loop — Hold, Bearing,
  sealing, ranking — is on the cheap side of that line.
- **History survives the collection.** Anki's own review log is one
  `Check Database` or one bad sync from being the only copy. `traces/` is
  committed, so `git log traces/` is a record of a subject being learned,
  and it outlives any single Anki profile.

The rejected alternative was reading `collection.anki2` directly, which
would give the full revlog (every grade, every timestamp) rather than the
per-card summary AnkiConnect returns. It was rejected because it means
parsing a schema Anki is free to change, and because the summary is
enough for every question currently asked. If per-review data is ever
needed — for an Elo-style estimate, or DAS3H-style time-window features —
it should arrive as a richer `pull`, still landing in the same file.
Nothing downstream should have to change.
