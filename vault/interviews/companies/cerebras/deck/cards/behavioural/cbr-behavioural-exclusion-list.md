---
id: cbr-behavioural-exclusion-list
node: behavioural.conflict
type: qa
step: 2
---
## Q
背景问题：Tell me about a time you disagreed with a teammate on quality. 用「拒绝把真问题加进排除名单」怎么讲？

## A
1. **Context**: my **daily health check** flagged settled transactions with **no fee** on a new payment path.
2. **The suggestion**: add that payment type to the check's **exclusion list** so the alert goes quiet.
3. **My position**: no — the fees were **genuinely missing**; excluding it would turn a **loud** detector **silent**.
4. **How I argued**: with **numbers anyone could re-run**: a control group with the field set had fees; the affected rows were **0% at every age**, so it wasn't lateness.
5. **Outcome**: the check stayed; root cause found (NULL plus a wrong overload); an end-to-end test added.
6. **Lesson**: "A check that fires on **missing data** is worth defending; the fix goes in the code, not the alert."

> 中文提示：这个故事同时可以答"pushing back on lowering a quality bar"。说"someone suggested"，不点名。
