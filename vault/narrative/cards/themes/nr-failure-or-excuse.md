---
id: nr-failure-or-excuse
node: themes.failure
type: qa
---
## Q
You have prepared a failure story. How do you tell whether it is a real failure or a disguised excuse — before an interviewer tells you?

## A
Run five tests. A disguised excuse fails at least two:

- **Name the cost.** Money, weeks, an outage, a person's trust. If the worst outcome is "it took longer than expected", that is a schedule, not a failure.
- **Are you the proximate cause?** Excuses have an external subject: requirements changed, the vendor was late. A real failure has *you* as the subject of the verb that caused it.
- **Would the other party tell it the same way?** If your version quietly makes them the problem, the interviewer will hear it.
- **Is the lesson a mechanism or an intention?** "I learned to communicate earlier" is worth nothing. "We now require a written rollback plan on any migration touching billing" is a mechanism.
- **Does it end with "but it worked out fine"?** That reflex undoes the whole answer.

The counter-intuitive part: **the better your failure story, the safer you are.** Candidates pick something harmless, which reads as evasive and invites a harder probe. A specific, costly, owned failure told calmly is one of the strongest signals in the loop, because almost nobody offers one.
