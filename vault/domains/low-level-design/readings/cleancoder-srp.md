---
nodes: [principles.solid]
url: https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html
tags: [canonical]
---
# The Single Responsibility Principle (Robert C. Martin)

The author of SOLID correcting the summary everyone repeats: SRP is not "a
class does one thing" — it is about *who asks for changes*, and this post is
the worked example that makes the other four principles fall into place.

**Extract on read:**
- The real statement: gather things that change for the same reason, separate
  things that change for different reasons — a module answers to one actor
  (CFO, COO, CTO), not to one verb.
- The violation to spot: `Employee` with `calculatePay`, `reportHours`, and
  `save` — three actors, so any one of them can break the others; the fix is
  splitting the behaviour out and keeping the data class.
- Why "do one thing" is the wrong test: applied to methods it is a different
  (and finer) rule than SRP, and applied literally to classes it produces the
  shallow-class explosion.

%% trellis:begin %%
## Source
[Open the original ↗](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html)

## Archived copy
![[cleancoder-srp-clip]]
%% trellis:end %%
