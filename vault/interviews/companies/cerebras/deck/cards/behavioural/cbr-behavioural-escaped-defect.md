---
id: cbr-behavioural-escaped-defect
node: behavioural.failure
type: qa
step: 2
---
## Q
背景问题：Tell me about a defect that escaped your tests. What changed afterwards? 怎么讲？

## A
1. **Escape**: fees went **silently missing** on a new payment path; our end-to-end tests were green.
2. **Caught by**: a **daily health check** I'd built — not by the tests.
3. **Why tests missed it — four reasons**:
   - tests asserted **routing**, not the **fee**;
   - the fixture was a **card payload**, not the new path;
   - pending rows never asserted the field;
   - nothing spanned **promote → fee**.
4. **What changed**: one function instead of two overloads; old signature **dropped** in a versioned migration; a new **end-to-end test across the whole chain**.
5. **Rule**: "The fixture must look like the **real population**; assert on the **output**; an unmappable input must **fail loudly**."
6. **Bridge**: "That's why I care about integration tests: each stage was green on its own."

> 中文提示：这是 RIT 职位里"issues discovered during final release qualification or production"的直接答案。
