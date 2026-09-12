# A corpus enters as readings on a skeleton it may have seeded; its deck is a filter

A book has a table of contents, and the obvious thing to do with it is to
make it the skeleton. ADR 0002 forbids exactly that for a codebase: the
result has the author's blind spots, and the parts of the subject they never
built are invisible in it. A book is the same trap with better prose — so
its outline stays its own thing, kept beside the skeleton and related to it
only by triage, section by leaf. What the book never reaches is the most
useful output of the exercise and is listed under the Corpus note, not lost.

**The relaxation.** A subject with no skeleton yet may be *seeded* from a
canonical book's outline. A field's definitive text is evidence about the
field in a way one team's repository is not. The draft is still judged the
way ADR 0002 demands — as an opinion about the subject, not a description of
the book — and the review adds the leaves the edition omits (the mechanism
that replaced one it describes, the question an interviewer asks that the
book does not). Those come back as `uncovered`, and because the corpus is
then triaged onto the finished skeleton like any other source, they show up
as leaves with nothing attached rather than disappearing. Seeding is refused
once a skeleton exists: an existing map grows from its gaps, by hand.

**A deck for the book is a filter, never a second deck.** A card's Anki note
GUID is a hash of its id and its deck is its leaf's place in the skeleton.
A book-shaped deck tree would either duplicate every note or move it out of
the hierarchy that gives it its study order. So the corpus view is the
domain's cards filtered by provenance — the same ids, the same review
history — plus a tag on every card, so a filtered deck inside Anki does the
same thing without a build.

**A book you paid for stays on the machine that read it.** Its text is
needed to triage and digest, and nowhere else. ADR 0001 commits clippings on
the argument that the repository is private and a clone is how the archive
reaches a phone; that argument covers an article, not a whole commercial
book. So `license: commercial` ingests into a gitignored directory, only
the outline (titles) is committed, readings for its sections carry a
locator instead of a clipping, and cards are written from the text but do
not copy it. Freely published material is archived and clipped as before.

**Consequences.** A domain can now be born from a book in an afternoon, but
its first review is the slow part and is not skippable. Two machines
digesting the same commercial corpus each need the file. The Corpus note is
the honest report of what a book taught and did not teach, and it changes
as cards are written, so it is generated, never edited.
