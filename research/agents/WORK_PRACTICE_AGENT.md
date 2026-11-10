# Work practice deck: how my team really does system design

Run this on the **work laptop**, with Claude Code (or another coding agent) next to the team's repositories. It turns the team's
code into a separate Anki deck that hangs on the same exam points as the system-design deck, so every fundamental has a
real example and an interview answer can use it directly. Reply to Chi in Chinese; code and files in English.

## What exists already

- `research/agents/sd_points.tsv`: the system-design exam points, heaviest first: `id`, domain, topic, point title, `core`,
  how many interview questions need it, and its prerequisites. This is the map; the work deck hangs on these ids.
- `vault/domains/hello-interview/系统设计 考点地图.md`: the same points as a mind map.
- The skill `distilling-work-into-domains` (`.claude/skills/`) holds the older, interview-safe flow for cases; this file
  replaces its "no cards" rule for this deck only, because Chi wants the practice itself to be studied.

## Where things go (never pushed)

Company material never goes to GitHub: the trellis repository is public.

- Workspace: `sources/local/work/<alias>/` (already gitignored). `<alias>` is a neutral name Chi picks.
- Deck skeleton `skeleton/work-<alias>.yaml` and cards `vault/domains/work-<alias>/`: add both to `.git/info/exclude`
  (local ignore, not committed) before writing anything, and check with `git status` that they do not show.
- Never `git add` them, never `git push` anything from this work.

## Steps (keep a ledger in `sources/local/work/<alias>/LEDGER.md`: one row per finished step, and the next action)

1. **Setup.** `git clone` the public trellis repository (or `git pull`), `uv sync`. Ask Chi for: the alias, the paths of
   the team's repositories, what the team owns, and his own role and projects. Write them to `sources/local/work/<alias>/README.md`.

2. **Inventory.** For each repository: services and their responsibilities, languages, data stores (schemas, keys,
   indexes), queues and topics, caches, external dependencies, API style, deployment and infra (Kubernetes, Helm,
   Terraform), configuration, docs, ADRs, runbooks and postmortems. Read in place; collect paths, not copies.
   Output `inventory.md`. Use `git log --author` to find Chi's own changes.

3. **Map onto the exam points.** Walk `sd_points.tsv` from the top. For each point the team's systems exercise, record in
   `points.md`: point id, where (repo, path, short SHA), what is done, why, the numbers (QPS, sizes, latencies, limits),
   what it costs or what went wrong, how it differs from the textbook answer, and Chi's own part. Mark every point
   **used**, **not used here**, or **ask Chi**. Practices with no matching point (an in-house framework, a team convention)
   go under **team-only**. Points heavy in `sd_points.tsv` but unused here are listed as **gaps**: the syllabus the job
   does not teach.

4. **Write the deck.** Domain `work-<alias>`, title `公司实践（<alias>）`, Chinese with English terms in parentheses.
   - Skeleton: the system-design domains → topics → only the points with evidence, then a `team-only` branch, then a
     `projects` branch for Chi's own projects. Every leaf for a catalog point carries the point id in its summary.
   - Cards, two to four per point, each self-contained and short (the rules of the system-design deck: one point per card,
     code never wraps, no filler):
     - **怎么做**: the mechanism in our system, where it lives, the numbers.
     - **为什么**: the choice against the alternatives, and what it costs.
     - **出过的问题 / 可以更好**: an incident, a limit, or where the practice falls short of best practice, and the fix.
     - **面试 30 秒版**: how Chi would tell it to an interviewer elsewhere, in general terms: no company, product, service,
       table or host names.
   - A project card per project in `projects`: situation, his decision, result with numbers, what he would change.
   - Tag every card `kp::<point id>` so it can be found from the system-design deck by point.
   - Gate: `uv run trellis --domain work-<alias> validate` shows 0 errors. Read every card once yourself.
   With more than about 40 points, split the points among at most 3 subagents, each with its own folder, and review
   their cards before accepting.

5. **Into Anki.** `uv run trellis --domain work-<alias> build -o sources/local/work/<alias>/work.apkg`, then import it in
   Anki (File → Import). The deck lands as `公司实践（<alias>）`. If Anki on this laptop syncs to Chi's AnkiWeb, it reaches his
   phone; that is his choice. Never run `anki_refresh.py` or `anki-push` for other domains from this laptop.

6. **Report to Chi:** points with practice, team-only practices, the top gaps by weight, and three practices most worth
   using in an interview.

7. **Keep it current.** On a later run, `git pull` the team repositories, diff against the SHAs in `points.md`, update the
   affected cards, rebuild and re-import (Anki updates notes by id and keeps their review history).
