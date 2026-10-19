---
id: nr-amz-s9-followups
node: amazon.s9
type: qa
step: 3
---
## Q
【Amex 出款延迟事故（事故指挥里的领域权威）】面试官会追问什么？每个怎么答？

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
