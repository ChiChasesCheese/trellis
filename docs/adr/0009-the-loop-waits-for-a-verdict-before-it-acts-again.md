# The loop waits for a verdict before it acts again

The loop was built arc by arc — `pull`, Hold, the Brief, `grow`, the
Workbench — and each arc worked. What was never run was the whole circle
with time passing through it. When it was, against the real collection on
2026-09-19, two things turned out to be true.

**It read age as forgetting.** Hold is read off the interval, and a card
shown for the first time yesterday has a one-day interval however well it
was answered. Of 71 leaves the loop called weak, 70 had no card that had
ever lapsed and none reviewed more than three times. The Brief was telling
the reader to repair topics they had merely started, and `grow` was writing
second routes into leaves where the first had not failed.

**It had no memory of having acted.** `grow` tags what it writes, and the
documentation promised the next Brief would "say whether the repair took",
but nothing read the tag. A weak leaf that had just been given four new
cards was exactly as weak on the next pull — the new cards were unreviewed
— so it stayed at the top of `grow --next`. A controller that answers the
same evidence twice is not a loop, it is a ratchet.

Both are the same mistake — treating a Trace that is not yet evidence as if
it were — and they get one fix.

## Every card has a verdict, and young is not one

`hold.verdict(trace)` puts a card in exactly one place:

- **unseen** — never shown.
- **young** — shown, never failed, below the bar, reviewed fewer than
  `SETTLED_REPS` (5) times. Its interval says how old it is.
- **taken** — its Hold is at or above the bar a leaf is judged against.
- **slipped** — below the bar, and it has lapsed, is relearning now, or has
  been reviewed five times and is still there. The last clause matters:
  Anki does not count a failure inside the learning steps as a lapse, and
  "Hard" never is one, so a card can be pulled back indefinitely without
  ever formally lapsing.

Only `taken` and `slipped` are evidence. A leaf's Hold is the mean over its
*judged* cards; young cards are left out the way unseen ones always were —
an absence of evidence, not a zero. `unproven` now means fewer than three
judged cards rather than fewer than three seen ones. And a Weakness needs at
least one card that slipped: shrinkage toward a struggling branch can carry
a leaf whose own cards all hold a hair under the line, and then there is
nothing for a second route to aim at.

Sealing follows without being touched. It reads the same rolled-up Hold, so
a young prerequisite now seals nothing — which is ADR 0005's own first
rule, *silence seals nothing*, applied to the other kind of silence.

The curve itself (`card_hold`) is unchanged. This ADR moves no threshold; it
decides which cards the thresholds are allowed to look at.

## A Graft is the loop reading its own tag back

The grown cards on a leaf are its **Graft**, and the same verdicts, counted
over just those cards, give it a state:

- **settling** — fewer than `min(3, grown)` of them have a verdict.
- **took** — judged, and more took than slipped.
- **slipped** — judged, and they failed the way the first route did.

A Weakness whose Graft is settling is withheld from `grow`: `plan` skips it,
`grow --leaf` refuses it and says what to review instead, the Workbench
disables the button and answers 409. The Brief's opening move for such a
leaf is **先复习**, with the Anki search for exactly those cards, instead of
**先做**. When the verdicts are in, the Brief says so under **新卡** — one
line each for what slipped or is still settling, one shared line for
everything that took, so good news can never crowd the page. A slipped Graft
leaves the leaf an ordinary Weakness again, and the next prompt carries the
grown cards that failed beside the original ones, so the third route differs
from both.

First cards on a leaf that had been uncovered are a Graft too — they carry
the tag — but not a *second* route, so they are not reported under 新卡.
They are simply the leaf's cards.

Nothing is recorded. A Graft is derived from `tags: [grown]` and the Traces
on every read, like everything else in the loop (ADR 0004): no "grown on"
date, no pending list, no state file to drift from the collection.

## What was considered and not done

- **A cooling-off period after growing** ("do not grow the same leaf for 14
  days"). It needs a date the vault would have to record, and it is the
  wrong variable: what matters is whether the cards were reviewed, which
  the Traces already say.
- **Fitting the young period to the scheduler** (FSRS stability, or the
  deck's actual learning steps). More faithful, and it would make Hold
  depend on collection settings that `pull` does not read. Five reviews is
  a constant with a reason attached; if it proves wrong it is one line.
- **Pushing automatically after `grow --import`.** The Workbench already
  offers it behind a review step. On the command line `anki-push` stays its
  own act: it syncs to AnkiWeb, and that should be typed, not implied.

## Risks worth recording

- A grown card that is suspended in Anki stays `unseen` forever, and its
  leaf stays settling. It is visible — the Brief names it on every
  regeneration — and the way out is to unsuspend or delete the card;
  `scaffold` and `digest` still write anywhere regardless.
- An all-grown leaf that later weakens and is grown on again cannot tell
  its second batch from its first. The gate still works (it only needs
  weak + unjudged grown cards); only the 新卡 line is lost for that leaf.
- The end-to-end test (`tests/test_loop_e2e.py`) replaces Anki with a fake
  that imports the real `.apkg`. While writing it, the CLI's `pull` and
  `anki-push` turned out to bypass the client the tests replace, and the
  fixture deck was imported into the live collection and synced. It was
  removed by note id. `tests/conftest.py` now makes the default client
  refuse inside the suite, so that cannot recur silently.
