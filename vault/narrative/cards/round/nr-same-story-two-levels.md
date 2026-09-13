---
id: nr-same-story-two-levels
node: round.seniority-ladder
type: qa
---
## Q
Two engineers tell the same story: an endpoint was slow, they profiled it, found an N+1 query, fixed it, latency dropped. The facts are identical. One reads as senior and one reads as mid-level. What are the differences that produce that gap?

## A
The gap is never in the technical work. It is in five places:

- **Where the story starts.** Mid-level starts at "I was assigned a slow endpoint." Senior starts at "I noticed our p99 alerts had been acknowledged and ignored for three weeks, and asked why."
- **Blast radius.** Mid-level fixed the endpoint. Senior asked how many other endpoints had the same shape, found nine, and fixed the ORM pattern or the lint rule that let it happen.
- **Who they had to move.** Mid-level stories have one actor. Senior stories have a person who had to be convinced.
- **What they said no to.** A deliberate cut. "I did not fix the other three because they were on a service being decommissioned" is a stronger sentence than fixing all four.
- **The cost they accepted.** Mid-level results are pure upside. Senior results have a price they chose to pay.

Blunt test on any story you own: **remove yourself from it and ask whether it still would have happened.** If yes, it is a task story, not an ownership story.
