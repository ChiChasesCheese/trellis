---
id: nr-amz-s10-followups
node: amazon.followups
type: qa
step: 46
---
## Q
<p class="title">退款费 billing-terms 复盘<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **How did you discover the predicate was wrong?**
    - 见待补
- **Who had seen your first number?**
    - 见待补
- **Why is the blast radius bounded?**
    - 切换后新 credit 自动拿到 **NET 计划 ID**；只有**切换前积压、切换后才跑**的商户受影响
- **How do you fix it?**
    - 费用创建时调 **`EFFECTIVE_PRICING_SCHEDULE(maid, date)`**；**不复制** credit 的历史计划 ID
- **What about the upstream lag?**
    - 函数按查询时**物理存在**的计划解析；批量铺开时滞后可能是**系统性**的；创建时重新解析**两者都缓解**
- **How do you know $5,854.52 is right?**
    - 口径 **`SUM(ABS(amount))/100`**；SQL 附录在复盘文档里
- **What changed in how you work?**
    - **每个结论一条可重跑查询**；爆炸半径谓词检查**时间有效性**

<div class="sources"><b>表达 · business English</b><br>• <b><i>reproducible</i></b> — 可复现的<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Every conclusion carries a reproducible query.”</span><br>• <b><i>time-validity</i></b> — 时间有效性<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The predicate needs a time-validity check, not just the current state.”</span><br>• <b><i>systemic lag</i></b> — 系统性滞后<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“In a bulk rollout, the upstream lag could be systemic.”</span></div>
