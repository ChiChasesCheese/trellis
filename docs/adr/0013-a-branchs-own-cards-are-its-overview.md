# A branch's own cards are its overview

Date: 2026-11-24.

A subject taught leaf by leaf loses its shape. An article on scaling writes became thirty-seven cards (twenty on its
sub-sections alone) and the learner, reading them one at a time, could no longer say what the article's four families of
methods were. The article's own structure was the thing missing, and there was nowhere to put it: cards belonged on
leaves, and a "summary" leaf is one more sibling among the detail.

So a card may sit on a node that has children. It is that branch's **overview**: what the branch contains, in the branch's
own order, complete and not deep.

- **Order.** A branch's own cards are met before anything below it (`sequence` walks the tree parent-first). Under
  core-first, a branch that holds a core leaf opens with its overview in the core pass.
- **Deck.** They file into the branch's own deck, or into the deck the skeleton names for them in `own_decks`
  (`node id -> deck path`). Only the node's own cards move; its subtree stays where it was. This lets the overviews of a
  whole domain be gathered in one deck and read through first, breadth before depth.
- **Depth is a level, not a tag.** How far down a card sits says how much detail it carries: branch = the frame, leaf =
  one piece of it. Nothing else marks an overview card (a `通览` tag on the card is only a convenience for searching).
- **A merged view may flatten the branch.** The system-design view re-hangs a page's leaves under a topic, so the page
  itself is gone from that tree; its generator brings the page back as the topic's first leaf, under the page's own id,
  so the same card file resolves in both skeletons.

Validation no longer warns about a card on a non-leaf node. An overview is still a card: it obeys every card rule, and
it must not become a second copy of the detail below it.
