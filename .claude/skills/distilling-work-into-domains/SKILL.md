---
name: distilling-work-into-domains
description: Use when the user wants to connect their real job, an employer codebase, or systems they built at work to trellis study domains (Kafka, Snowflake, system design), turn work experience into cases or interview stories, or learn fundamentals from what they shipped.
---

# Distilling Work into Domains

Work is the strongest memory hook the learner has: a partition key they chose, a warehouse they
resized, an outage they debugged. This skill hangs that experience on domain leaves as
**cases** (ADR 0003), so each fundamental is remembered through something real.

It runs on the work laptop, next to the employer's code, and keeps two tiers apart:

| Tier | Where | Holds | Leaves the machine |
|---|---|---|---|
| **Private** | `sources/local/work/<alias>/` (gitignored with `sources/local/`) | real names, file paths, short SHAs, numbers, the learner's PRs | never |
| **Interview-safe** | `vault/<domain>/cases/`, `vault/interviews/core/stories/` | the decision and its reasoning in the domain's vocabulary, dated by month | only after the learner approves the diff |

**Interview-safe** means: every sentence is one the learner would say to an interviewer at another
company. The employer's code, identifiers and data stay in the private tier.

## Steps

1. **Prepare.** `git pull` on main. Confirm `git check-ignore -q sources/local/work/probe` succeeds.
   Ask the learner two things and record the answers in `sources/local/work/README.md`: whether
   their employer's policy allows interview-safe summaries of their own work in a personal repo;
   and a denylist of terms that must
   never leave the machine — company, product, team, service, topic and table names, internal
   hosts, ticket prefixes — one per line in `sources/local/work/denylist.txt`.
   *Done when* both files exist and the policy answer is written down. When the answer is no or
   unsure, do steps 2–4 for private study on this machine and skip steps 5–7: nothing is staged.

2. **Map work onto the field.** Pick one system and its domains (a pricing service → `kafka`;
   a data pipeline into Snowflake → the Snowflake domain). List the leaves from
   `skeleton/<domain>.yaml` that the system could exercise. The skeleton leads, the code answers
   (ADR 0002). If the domain has no skeleton yet, build it first with `building-study-domains`.
   *Done when* the candidate leaf list is written in `sources/local/work/<alias>/leaves.md`.

3. **Read the code in place, write private notes.** For each candidate leaf find the concrete
   decision: config, code path, incident, migration, dashboard. Kafka examples: producer `acks`
   and idempotence, partition key, consumer group layout, retry and dead-letter handling,
   compaction, schema evolution. Snowflake examples: warehouse size and auto-suspend, clustering
   keys, streams and tasks, COPY or Snowpipe loading, time travel retention, cost attribution.
   For each, write in `leaves.md`: leaf id, file path and short SHA, what was chosen, why, what
   broke or was traded off, numbers, and the learner's own commits or PRs. Reference code by path;
   leave the code itself in the employer's repo.
   *Done when* every candidate leaf is marked **evidence** (with a note), **unused here**, or
   **question for the learner**.

4. **Report the gaps.** Leaves with no evidence are the learner's syllabus: fundamentals they have
   not had to use. List them for the learner in the chat and in `leaves.md`.

5. **Write interview-safe cases.** One case per evidence note, in `vault/<domain>/cases/<slug>.md`,
   shaped like the existing ones in `vault/system-design/cases/`: frontmatter `nodes`, `title`,
   `codebase: work-<neutral-alias>`, `ref: <YYYY-MM the decision was read>`,
   `artefact: work:<generic decision kind>`; the employer repo's paths and SHAs stay in `leaves.md`;
   body = the problem in general terms, the options, the choice and its reasoning in the leaf's
   vocabulary, what it cost, what the learner would do differently. Round numbers to an order of
   magnitude. Then extend the matching story in `vault/interviews/core/stories/` with a link to the case.
   *Done when* `uv run trellis --all validate` has 0 errors.

6. **Grow cards beside the cases.** A case is evidence and never becomes a card itself. When a case
   exposes a fundamental the deck lacks, write a discrimination card on that leaf through
   `trellis grow --leaf <domain>:<leaf>` or `trellis scaffold` → `trellis import`.

7. **Review gate.** Stage only interview-safe files, then run:
   `git diff --cached | grep -i -F -f sources/local/work/denylist.txt`
   It must print nothing. Show the learner `git diff --cached --stat` and every new file in full.
   Commit and push only after the learner says yes.
   *Done when* the learner has approved and the push succeeded, or the learner chose to keep it local.

## Common mistakes

- Pasting a snippet "just for context": code belongs to the employer; describe the decision instead.
- Names that feel harmless (a topic name, a table name, a dashboard title): they are on the denylist for a reason.
- Deriving a new skeleton from the codebase: the gaps disappear with it.
- Writing "we decided X" cards: they test recall of one team's conclusion, not the fundamental.
