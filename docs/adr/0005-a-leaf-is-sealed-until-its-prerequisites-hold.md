# A leaf is sealed until its prerequisites hold

The skeleton has always carried `requires` edges, and validation has
always used them for one thing: guaranteeing that tree order never puts a
node before something it needs. That makes the *authoring* order
coherent. It does nothing about the *studying* order, because being
shown Consensus after Replication is no help if Replication never took.

So a leaf whose prerequisites are not holding is **sealed**: its cards
exist, are built, and are withheld from the Feed until the ground under
them takes. This is what makes the curve smooth rather than merely
ordered.

Three things make this safe enough to do automatically:

- **Silence seals nothing.** A prerequisite with no Traces is not a
  failing grade. Without this rule a fresh collection would seal the
  entire skeleton on day one, which is the obvious way this idea fails.
- **The threshold is low.** A prerequisite has to be *taken*, not
  perfected — deliberately below what anyone would call "known", because
  a strict gate produces a system that never opens anything.
- **Sealing hides, it never deletes.** The cards are in the collection
  and in the deck tree; only the Feed's search excludes them, and
  `trellis feed --include-sealed` turns it off entirely. Nothing is
  unrecoverable and nothing is hidden from Anki itself.

The alternative was to show everything and trust the scheduler, which is
what Anki does by default and what every other markdown→Anki tool does.
It was rejected for a specific reason: the failure it produces is
invisible. Cards from a topic you were not ready for do not announce
themselves; they just lapse, over and over, and read as "I am bad at
this" rather than "this arrived too early". Sealing converts that into a
line in the Brief naming the topic that actually needs the work.

The risk worth recording: sealing is only as good as the `requires`
graph, and that graph is thin — a hundred nodes with twenty-two edges in
`system-design`, ten in `basketball`. Where the edges are missing,
sealing silently does nothing. Adding edges is therefore not tidying; it
is the input this feature runs on.
