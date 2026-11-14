---
id: cbr-behavioural-region-conditional
node: behavioural.conflict
type: qa
step: 1
---
## Q
背景问题：Tell me about a disagreement with a senior engineer or your manager. 用 S9（出款延迟事故）怎么讲？

## A
1. **Situation**: a large marketplace merchant reported roughly **$4M** of Amex payouts "missing"; a formal incident; I was named **one of three** fix owners.
2. **My authority piece**: a senior teammate said he lacked context on the US SLA and **deferred to me**; I established that **T+7 is our internal SLA** and we pay out only after Amex settles to us — separating **expected latency** from the **real regression**.
3. **The disagreement**: the regression was an EU-compliance date change that shifted US payouts by a day. **Revert** was fast; I argued for a **region conditional** so EU and US keep **independent semantics**.
4. **How**: the trade-off in writing — fast vs robust — and the group chose the conditional.
5. **Boundary**: teammates deployed it; I **stayed out of the deploy step**. Closed in **three days**.
6. **Lesson**: "Settle the **boundary** first; then the conflict mostly dissolves."

> 中文提示：不点商户名和同事名。追问"如果你输了怎么办"：【待补：一个你让步并全力执行的真实例子】，没有就如实说"my strongest examples are ones where the group agreed"。
