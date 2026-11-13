---
id: nr-influence-what-moves-a-team
node: themes.influence
type: qa
---
## Q
You need another team to change something — fix the flaky tests that keep blocking your release, adopt a new test gate, add an API you depend on. None of them report to you, and they have their own roadmap. What actually moves a team like that, in roughly the order you should try it?

## A
Authority is the one lever you lack, so use the others, cheapest first:

- **Their goal, in their terms.** Find what they are measured on and show how your ask serves it: "these three flaky tests also fail *your* presubmit twice a week."
- **Data they cannot argue with.** A small table beats a meeting: failure counts, hours lost, which release slipped. Make the cost visible to *them*, not just to you.
- **Make yes cheap.** Write the first PR, the migration script or the design doc yourself, so the decision becomes "review this" instead of "staff this".
- **A smaller first ask.** One component, one sprint, behind a flag. A reversible pilot is easy to approve and creates the evidence for the rest.
- **Allies before the room.** Talk to the engineer who feels the pain and the lead who sets priorities separately, before any group meeting where positions harden.
- **Escalation, done jointly.** If priorities truly conflict, write both positions down and take them up together: "we disagree on priority; here are the trade-offs." That is a decision request, not a complaint.

What interviewers listen for is that you **changed the other team's incentives or costs**, not that you out-argued them, and that the relationship was intact afterwards.
