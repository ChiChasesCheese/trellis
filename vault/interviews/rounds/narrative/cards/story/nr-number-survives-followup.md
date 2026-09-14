---
id: nr-number-survives-followup
node: story.numbers
type: qa
---
## Q
You say "I cut p99 latency by 40%." The interviewer says, "How did you measure that?" What must a number in your story be able to survive — and what do you say when you honestly don't have one?

## A
A number invites exactly one follow-up, and a number that dies under it is worse than no number at all. Before you use one, be able to answer:

- **Baseline** — 40% from what, on what date?
- **Instrument** — server-side histogram, client RUM, or a load test? Each measures a different thing.
- **Window** — over what period, like-for-like? A week-over-week spanning a holiday measures the holiday.
- **Confound** — the honest one. "Traffic also dropped 10% that week, so I'd call it 30–40%." Volunteering it *raises* your credibility more than the clean number would have.
- **The bar** — what result would have made you revert.

**When you don't have a number** — common and fine — do not invent one. Substitute a **countable fact**: "I don't have the exact figure, but the pager for that service went from about three wakeups a week to none for the two months before I left." Countable, checkable, never penalised. The only losing move is a confident round number you cannot back up.
