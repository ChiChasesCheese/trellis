---
id: nr-amz-s9-followups
node: amazon.followups
type: qa
step: 41
---
## Q
<p class="title">Amex 出款延迟事故<span class="meta">03 追问</span></p>

面试官会追问什么？每个怎么答？

## A
- **What exactly did you do vs. the others?**
    - **One of three owners**；我的是 **SLA determination** + **fix direction**；修复由两位同事部署
- **How did you know T+7 is the internal SLA?**
    - 见待补
- **Why a region conditional over revert?**
    - revert 会把 **EU 合规改动**也撤掉；条件分支让 **EU/US 语义独立**
    - 代价：UDTF 里多一个分支 + 测试，覆盖方式见待补
- **Did the merchant get their money?**
    - 见待补
- **What changed afterward so this wouldn't repeat?**
    - 见待补；不说「上游时序不是故障」
- **Whose PR caused it?**
    - **我们自己团队**的改动，不点名；说 "an effective-date change we made for EU compliance"
- **How did you handle disagreement in the channel?**
    - **把边界讲清楚**，冲突就消解了；没有挤进部署

<div class="sources"><b>表达 · business English</b><br>• <b><i>scope of ownership</i></b> — 负责范围<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“My scope of ownership was the SLA determination and the fix direction; two teammates deployed.”</span><br>• <b><i>independent semantics</i></b> — 语义相互独立<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A region conditional keeps EU and US semantics independent.”</span><br>• <b><i>trade-off</i></b> — 取舍<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The trade-off is an extra branch and its tests, in exchange for not undoing the EU compliance change.”</span></div>
