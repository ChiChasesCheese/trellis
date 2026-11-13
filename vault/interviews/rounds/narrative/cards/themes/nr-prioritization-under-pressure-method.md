---
id: nr-prioritization-under-pressure-method
node: themes.prioritization
type: qa
---
## Q
It is six hours before a release cut. Forty test failures are open, two engineers are available, and the requirements for one feature are still ambiguous. What method do you use to decide what to work on, and how do you communicate it?

## A
**First sort by the one question that matters at a deadline: "would this stop the release?"** Then spend effort only where the answer is unknown.

- **Triage before fixing.** Spend the first 30–45 minutes classifying all forty, not fixing the first one: new regression, known issue, flaky, infrastructure, test bug. Group failures with the same signature; forty often collapse into six causes.
- **Rank the causes** by impact if shipped × likelihood it is real × how long it takes to know. A five-minute rerun that settles a likely flake goes before a two-hour investigation.
- **Time-box the unknowns.** "One hour on the crash; if we cannot explain it by then, it becomes a release blocker by default." A default decision prevents drift.
- **Resolve ambiguity by asking, cheaply.** Write the two interpretations in one message to the feature owner with your recommended default and a deadline for objections.
- **Communicate options, not problems.** "We can ship on time without feature X, or ship X a day late; here is the risk of each." Let the owner choose the trade-off; you own the analysis.
- **Write the cut down.** A short list of what was deferred and who agreed, posted where the release is tracked.

The method is the answer: classify, rank, time-box, offer options, record the cut.
