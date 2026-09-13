# Adopted notes stay with their owner; the Workbench is a local page over the CLI

Two decisions that look unrelated share one principle: Trellis takes on
no ownership it cannot honour.

**A deck written by another tool is adopted, not taken over.** The
LeetCode deck was written straight into Anki by a generator whose vault
is not on this machine. The obvious move was to import its notes as
ordinary cards and let `build` and `anki-push` treat them like any other.
That would put a second copy of every note in the collection (a Trellis
GUID is a hash of a card id; the generator's GUIDs are its own), and the
first time the generator re-imported, the two copies would diverge. So an
adopted card is a mirror: it carries the note's id in `anki:`, sits on a
leaf so its Trace reaches the loop and `grow` can write beside it, and is
skipped by `build`; `align` never moves a note tagged `trellis::adopted`.
What Trellis does write into Anki is two tags — the id and the node — so
`pull` can read the note back. The cost is that an adopted card's text
in the vault is a snapshot; re-running `adopt --anki` refreshes it.

**The Workbench runs on this machine and only does what the CLI does.**
The loop needs a surface a person will actually use in the two minutes
they have: see what is weak, say what to write, watch it land. A hosted
page or a bundled app would need an account, a deploy and a second copy
of the state. The page is served by `trellis serve` from the repository
it sits in, talks to Anki through the same AnkiConnect client the CLI
uses, and asks Claude Code on this machine to answer prompts through the
same `claude` binary a terminal would. Every button corresponds to a
command, and the tests drive the page's API with Anki and the Runner
replaced by fakes — which is what makes a local page cheaper to trust
than a remote one.

**Consequences.** Adopting a deck is safe to repeat and safe to undo (delete
the mirrors; the tags are inert). The Workbench has no state of its own
beyond a job list under `.trellis/jobs/`; closing the terminal closes it,
and nothing is lost. Anything the page can do can be done without it.
