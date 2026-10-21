---
id: nr-amz-s4-followups
node: amazon.followups
type: qa
step: 16
---
## Q
<p class="title">澳洲 Amex 退款费<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **How did you know it wasn't a regression?**
    - 上游**出款服务**从来没为 AU direct-Amex 发过退款费；迁移里变的只有**报表**
- **Why did you pull data rather than discuss?**
    - 争论源于领域知识不对称；数据让所有人**当场可验证**
- **What was the second issue?**
    - AU-only `refund` 费用种类；我说**不确定**，给分层假设和验证方法；资深同事确认
- **What did you do for the merchants in the meantime?**
    - 见待补
- **What if the data had contradicted your guess?**
    - 方法不变：结论由**查询**给出，不由我给出
- **Who owns the new feature? How big is the money?**
    - 见待补

<div class="sources"><b>表达 · business English</b><br>• <b><i>layered hypothesis</i></b> — 分层假设（逐层列出可能原因及验证方式）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“For the second fee kind I offered a layered hypothesis and how to verify each layer.”</span><br>• <b><i>not sure yet</i></b> — 目前还不确定<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I&#x27;d rather say not sure yet with a plan than guess.”</span><br>• <b><i>regression</i></b> — 回归（以前没问题，改动后才出错）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I proved it was not a regression, because the payout service never issued those fees.”</span></div>
