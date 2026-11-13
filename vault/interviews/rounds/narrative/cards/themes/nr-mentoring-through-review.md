---
id: nr-mentoring-through-review
node: themes.mentoring
type: qa
---
## Q
"How do you raise the bar of the engineers around you?" You want to talk about code review. What separates review as mentoring from review as gatekeeping, in concrete habits?

## A
**Gatekeeping catches this change's bugs. Mentoring changes the next hundred changes.** The habits that show the difference:

- **Explain the principle, not just the fix.** "This test sleeps two seconds, so it will flake under load; wait on the condition instead" teaches something reusable. "Change to `wait_for`" does not.
- **Label severity.** Mark each comment as blocking, suggestion or nit, so a junior engineer knows what must change and does not treat taste as law.
- **Ask before asserting** when you might be missing context: "what happens if this retries after the job already committed?" They find the bug themselves and remember it.
- **Move big issues out of the thread.** A design problem in comment 14 of a 900-line diff is a 20-minute call, then a short written summary.
- **Turn repeated comments into mechanisms.** The third time you write the same comment, make it a lint rule, a test helper or a page in the team guide.
- **Hand over the reviewer role.** Ask the person you mentor to review your changes and others'; their comments show whether the standard has transferred.

Measured signals: fewer repeat comments over time, smaller and better-tested changes from that person, and them catching issues in other people's reviews.
