# The Atlas reads a Snapshot; Traces stay local

The trellis gets a public face, the Atlas: a static site on GitHub Pages that shows every published domain as a
map and as a directory, with how far each node has been studied, and lets anyone read its cards (Chi, 2026-11-28).
It is built in three layers that only talk through files: the engine (`trellis export`) writes a data contract
(JSON, Markdown, JSON Schema), and the views (an Astro site) read only that contract, never the vault or a
skeleton. Agents read the same contract, so what a person sees and what an agent parses cannot drift apart.

What it shows of the learning is a **Snapshot**, never a Trace. A Snapshot is per node and dated to the day:
Reach, Hold, the Weakness, uncovered and sealed flags, and how many cards were studied that day. Traces carry
per-card millisecond review times, which tell anyone when Chi studies and sleeps; they leave git and stay on the
machine that pulls them, and the committed Snapshot history becomes the dated record of a subject being learned
that `git log traces/` was in ADR 0004 (the Workbench's history reads it too).

The colour is **Reach**, not Hold: the share of a node's cards studied at least once, counting a test question as
a reading of the card on its back. Chi wanted the map to say "I have been through this", in green that deepens
with the share, and one sentence on the page can define it. Hold stays the loop's measure and is published beside
it, not as the colour.

What may be published is an allowlist (`atlas.yaml`): domains by name, minus the branches and leaves that belong
to a company (the company decks, `narrative` `amazon`, `hello-interview` `tt` and `fix`, `code-core`
`transfer.<co>`), with company tags stripped. A check fails the build when a published id, path or tag names a
company from `vault/interviews/companies/`, so new company material cannot leak by default.

## Considered options

- **Quartz over the vault.** The best Obsidian fidelity for the least work, but the mastery map, the directory
  switch, presenting, in-browser study and the agent contract all sit outside what it is built for, and a
  framework made of trellis plus a Quartz fork is heavier for anyone else to adopt.
- **Publishing Traces as they are.** No new format, but a public record of study hours, and a site would have to
  re-implement `hold.py` in the browser.
- **Hold as the colour.** It is the better measure of retention, but it needs a paragraph to explain and drops when a
  card is forgotten, which reads as decline to someone who skims.
