# Trellis

A skeleton-constrained knowledge base for interview-grade study: one mind map
per subject decides what exists and in what order, and every piece of content —
recall prompts, source material, practice — hangs off a node of it.

## Language

### The map

**Skeleton**:
The single YAML mind map for one subject, and the only source of truth for what
topics exist, their study order, and their prerequisites.
_Avoid_: tree, outline, syllabus, curriculum

**Node**:
One topic in the skeleton. Its position fixes where its content is studied and
which Anki deck that content lands in.
_Avoid_: chapter, section, category

**Leaf**:
A node with no children — the unit content attaches to. A leaf is one interview
probe: narrow enough that "I'm weak here" names something specific to drill.
_Avoid_: subtopic, bucket

**Prerequisite**:
A `requires` edge from one node to another that must be understood first.
Validation guarantees no node is ordered before one of its prerequisites.
_Avoid_: dependency, blocker

**Domain**:
One subject with its own skeleton and content — `system-design`,
`low-level-design`. Domains are independent; nothing crosses between them except
ordinary wikilinks.
_Avoid_: deck, subject, area, vault

### The content

**Card**:
An atomic recall prompt (question/answer or cloze) attached to exactly one leaf.
The thing reviewed in spare minutes.
_Avoid_: note, flashcard, item

**Reading**:
A pointer to one authoritative external resource — its URL, why it is worth
reading, and what to take from it. Attaches to one or more nodes and is written
by us.
_Avoid_: link, source, reference, resource

**Clipping**:
A local markdown copy of the page a Reading points at, stored in the vault so
the material can be read offline inside Obsidian. Matched to its Reading by the
`source` URL, whether it was produced by `trellis clip` or by Obsidian's Web
Clipper.
_Avoid_: archive, cache, snapshot, offline copy

**Drill**:
An exercise that trains producing an answer rather than recalling one — a design
question or coding problem with constraints, grading points, and an attempt log.
Spans several nodes.
_Avoid_: exercise, problem, practice question

### The surfaces

**Vault**:
The one Obsidian vault at `vault/`, holding every domain, organised by purpose:
subjects under `domains/`, interview material under `interviews/` (ADR 0008). A
domain's folder inside it is its *content directory*, declared by the skeleton's
`vault:` key, never "its vault".
_Avoid_: notes folder, library

**Map note**:
A generated note mirroring one node, listing its prerequisites, children, cards,
readings, and drills. Everything outside its managed block is the reader's own.
_Avoid_: index note, MOC, hub

**Feed**:
A deck built to be reviewed rather than authored: one stream across every
Domain, ordered so that consecutive cards come from different subjects. The
surface for spare minutes, where the Brief is the surface for deciding.
_Avoid_: mix, shuffle, stream, playlist, feed deck

**Go deeper**:
The footer on a built card carrying its node's readings — as `obsidian://` links
when the reading has been clipped, and as web links otherwise.
_Avoid_: sources, further reading, references

**Readable source**:
A reading whose page is archived in the vault as real prose (or as the paper
itself) and that is not a pointer at a book or an index. Engineering blogs,
company write-ups, papers, and single sections of a knowledge base qualify; a
book's homepage does not, unless what is archived is the chapter itself.
_Avoid_: good source, primary source

**Link coverage**:
The share of cards that have a road onward — an inline link, or a reading
inherited from their node or its ancestors. Tracked because a card with no way
deeper is a gap in the index.
_Avoid_: link rate, source coverage

**Card coverage**:
The share of leaves carrying at least one card. An uncovered leaf offers
nothing to review, so nothing can ever be learned about how well it is known —
which is what separates it from a [Weakness], a leaf whose cards exist and
fail.
_Avoid_: gap, completeness, fill rate

### The loop

Everything above flows one way: a skeleton decides, content hangs off it, a
deck is built. These are the terms for the way back — what reviewing a card
teaches the trellis about itself.

**Trace**:
One card's review history as Anki recorded it: how many times it was answered,
how often it lapsed, and how it is scheduled now. A Trace is pulled, never
authored — it is the only thing in the vault we do not write.
_Avoid_: stats, history, telemetry, metrics

**Verdict**:
What one card's Trace is evidence of: *unseen*, *young* (shown, never failed,
too new for its short interval to mean anything), *taken*, or *slipped*. Only
the last two are evidence; a young card is no score at all, not a low one
(ADR 0009).
_Avoid_: status, grade, result, state (of a card)

**Hold**:
How well a node is retained, computed from the Traces of the cards beneath it
that have reached a Verdict, and rolled up the skeleton. A leaf holds or it
does not; a branch's hold is its leaves'. Always measured, never declared.
_Avoid_: retention, mastery, score, strength, level

**Weakness**:
A leaf with enough Verdicts to judge, a Hold below target, and at least one
card that slipped. A Weakness wants practice — a drill, a reading, more cards.
Distinct from an uncovered leaf, which has nothing to fail and wants writing
instead, and from a leaf that is merely new, which wants only time.
_Avoid_: gap, weak spot, problem area, struggle

**Bearing**:
How much of the skeleton rests on a node — the nodes that reach it through
`requires`, directly or transitively. A load-bearing Weakness is the first
thing worth repairing, because everything standing on it is repaired with it.
_Avoid_: importance, priority, centrality, leverage, weight

**Sealed**:
A leaf whose prerequisites do not yet Hold. Its cards exist and are withheld,
so nothing new is ever introduced on ground that has not taken. Sealing is what
makes the study curve smooth rather than merely ordered.
_Avoid_: locked, blocked, gated, not ready

**Brief**:
The one generated note that says what to do next: the load-bearing Weaknesses,
the leaves worth writing for, and a single opening move. Derived from Traces on
every regeneration, and short enough to read standing up.
_Avoid_: dashboard, report, summary, digest, progress

**Graft**:
The grown cards on one leaf, and what reviewing them has shown: *settling*
while too few have a Verdict, then *took* or *slipped*. A Weakness whose Graft
is settling has been answered and not yet heard back from, so nothing more is
grown on it; the Brief asks for the new cards to be reviewed instead. Derived
from the `grown` tag and the Traces, recorded nowhere.
_Avoid_: repair, fix, patch, batch, second route (as the noun for the cards)

**Adopted card**:
A card whose note lives in Anki and was authored by another tool. Trellis holds
a mirror of it — placed on a leaf, read for its Trace, grown beside — and never
builds, pushes or moves it; the other tool keeps owning the note.
_Avoid_: imported card, foreign card, external card, mirror (as a noun)

**Guidance**:
Free text the learner attaches to a grow request — what to emphasise, which
angle to take, what context to bring — appended to the prompt as it is.
_Avoid_: instruction, hint, context, prompt

**Runner**:
What answers a prompt: Claude Code on this machine, or a person pasting JSON.
Trellis never calls a model directly; it hands a prompt to a Runner and
validates what comes back.
_Avoid_: LLM, model, generator, agent

**Focus**:
A leaf the learner has chosen to study now: its cards are made due today, its
weak spots are grown first. A Focus is an act on the collection, not a state
the vault records.
_Avoid_: priority, pin, spotlight, filter

**Workbench**:
The local page that shows the loop and lets the learner act on it — see every
domain's Hold at once, pull, read the Brief, grow with Guidance, Focus, open a
leaf in Obsidian or Anki. It does only what the command line does.
_Avoid_: dashboard, app, UI, console, frontend

**Grow**:
Writing new cards where the loop says it pays: for a Weakness, cards that reach
the mechanism from another angle than the ones that slipped; for an uncovered
leaf, its first cards. Grounded in what the vault already holds for the leaf —
a corpus's sections or a clipped reading — and never anywhere the loop did not
point, and never on a leaf whose Graft is still settling. A grown card is
tagged so the next Brief can say whether the Graft took.
_Avoid_: generate, populate, backfill, fill in, repair (for the act of writing)

### Ingesting a codebase

**Codebase**:
A repository studied as a learning target, declared by one `codebases/<name>.yaml`
that maps its paths to what they hold. The repository itself stays where it is;
nothing here is a fork of it.
_Avoid_: source, project, target repo

**Lens**:
The angle a codebase is examined through — `system-design`, `low-level-design`,
`quant-infra`, `markets`. A lens decides which skeleton an artefact attaches to
and, more importantly, in whose vocabulary it gets rewritten.
_Avoid_: perspective, view, angle

**Harvest kind**:
What a declared path holds, and therefore how it is treated: `contracts` and
`decisions` become Cases, `subject` becomes readings and clippings, `glossary`
is only compared against our own language.
_Avoid_: category, type, material

**Triage**:
Deciding, artefact by artefact or section by section, which lens and which
leaf a piece of a codebase or a corpus belongs to and what it should become.
Produces a proposal for review, never writes into the vault directly.
_Avoid_: import, classification

**Case**:
A decision taken from a codebase and rewritten in a lens's vocabulary, frozen at
the commit it was read from. It attaches to an existing leaf as evidence — "a
real system did this" — and is read like a reading. It is never a copy of the
artefact and never restates it as a card.
_Avoid_: example, sample, exhibit, snippet

**Gap**:
An artefact or section triage could not place on any leaf — a proposal to
grow the skeleton, not an error. Gaps are the point of mapping a codebase or
a corpus onto a skeleton authored independently of it. A leaf that merely has
no cards is not a Gap; that is [card coverage].
_Avoid_: miss, unmatched, hole

### Digesting a corpus

**Corpus**:
One body of material registered for digestion — a book as an epub, a pdf, or
freely published chapters; a blog series; a course. Declared by one
`corpora/<id>.yaml`. Its license decides whether its text may be committed.
_Avoid_: book, material, source, text

**Outline**:
A corpus's own hierarchy of sections, as its author organised it. It is never
the skeleton and never becomes one by copying; the two are related only
through triage.
_Avoid_: table of contents, ToC, structure

**Section**:
The unit a corpus is split into — a chapter, or a heading below it, as the
outline defines. What triage places.
_Avoid_: chapter, part, page range, chunk

**Ingest**:
Turning a registered corpus into archived sections plus its outline,
resumable where fetching is involved.
_Avoid_: download, extract, parse

**Seed**:
Drafting a skeleton for a subject that has none from a canonical corpus's
outline, then reviewing the draft as a map of the field. The corpus is
triaged onto the result like any other; what it never reaches is listed, not
lost.
_Avoid_: derive, generate, bootstrap

**Digest**:
Writing cards leaf by leaf from the sections triaged onto that leaf. Produces
prompts and validates answers; never writes into the vault on its own. A leaf
is done when cards from the corpus exist on it — nothing else records it.
_Avoid_: generation, card writing

**Provenance**:
The corpus, and where possible the section, a card or reading was written
from. Carried in the note's frontmatter and shown as an Anki tag.
_Avoid_: origin, attribution, citation

**Corpus view**:
The subset of a domain's content that came from one corpus — a filtered build
and a generated note. The same cards with the same identities, never a second
deck.
_Avoid_: book deck, corpus deck

**Language**:
The language a domain is written in. A domain has one; a card is in it, and
may carry an appended translation. There is no "original" language a domain
must be written in first.
_Avoid_: locale, translation (for the primary text)
