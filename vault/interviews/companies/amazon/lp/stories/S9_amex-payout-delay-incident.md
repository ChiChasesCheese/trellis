# S9 · Amex 出款延迟事故（事故指挥里的领域权威）

**A large marketplace merchant reported about four million dollars of Amex payouts "missing"; I was named one of three fix owners and separated expected latency from the real regression.**

## 适用 LP

- 主：**Customer Obsession**
- 副：Dive Deep、Have Backbone、Earn Trust、Deliver Results、Ownership、Insist on the Highest Standards

## 数字

- 商户报告 **~$4M** Amex 出款"不见了"（延迟，不是丢失）
- **三位 fix owner 之一**，由指挥点名
- **T+7** = 内部管线 SLA（美国 aggregated Amex）
- **6/23** 一次 Agg-Amex effective-date 改动（为 EU 合规）把 US 出款日推后 **~1 天**：真实根因
- 事故 **07-06 → 07-09** 关闭，**三天**

## S / T / A / R / L

### S
- 大型 marketplace 商户报告约 **$4M** Amex 出款"不见了"
- 开了**正式事故频道**

### T
- 指挥点名我是**三位 fix owner 之一**
- 我的任务：判断这是**违约**还是预期延迟，并修真正的原因

### A
- 资深同事对美国 aggregated-Amex SLA **没有背景**，**让我来答**
- 我说明 **T+7 是内部管线 SLA**，且我们**只在 Amex 结算到我们之后才出款**
- 这就分开了**预期延迟**和**真实回归**，终止了「是否违约」的争论
- 指挥追到 **6 月 23 日**为 **EU 合规**做的 effective-date 改动，把 US 出款推后约**一天**
- revert 最快；我主张在 table function 里加 **region 条件**，EU 和 US 语义相互独立
- 小组选了它；**两位同事部署**了修复

### R
- 事故**三天内关闭**
- 我的份额：**SLA 判定**和**修复方向**；部署是同事做的

### L
- 多 owner 事故里，拿下自己是**权威**的那一块，**直白**地说
- 争取**稳健**的修法，而不是最快的

## 追问与回答

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

## 换个 LP 讲

- **Customer Obsession**：以商户的预期为起点，第一件事是告诉他们这是不是真的；区分延迟 vs 回归；没有商户反馈数据，别编
- **Dive Deep**：问题不是「慢不慢」，而是「SLA 是什么、6 月 23 日改了什么」；内部 SLA 与上游到账的边界
- **Have Backbone**：revert 是快路径，我主张不用；强调 robust；注意这不是 disagree-and-commit，且是小组选定的
- **Earn Trust**：资深同事让我答，所以我只说自己权威且可核对的部分，不越界
- **Deliver Results**：07-06 → 07-09 三天关闭；部署是同事做的，别说成我的
- **Ownership**：三位 owner 之一，只拿自己是权威的那一块，明确划线；别声称「我修好了」

## 待补

- 【待补：T+7 SLA 的出处（设计文档/runbook），以及如何确认「只在 Amex 结算到账后才出款」】
- 【待补：region 条件分支的测试怎么覆盖】
- 【待补：最终出款/是否补偿；确认 $4M 是延迟不是丢失】
- 【待补：事后 action item（SLA 文档、effective-date 变更的双区域测试、告警）】
- 【待补：有没有人主张 revert、是谁（角色）、你如何论证、结果是否被采纳；若你的意见被否决你如何执行（disagree-and-commit）】

<details><summary>逐字稿</summary>

> A large marketplace merchant reported roughly four million dollars of Amex payouts "missing," and a formal incident channel spun up. The incident commander named me one of three engineers who own the fix.
>
> I made two contributions. First, the SLA. A senior teammate said he didn't have context on US aggregated-Amex SLAs and deferred to me. I established that T+7 is our internal pipeline SLA for the US, and that we only disburse after Amex settles funds to our account. That separated expected latency from a real regression, which stopped the argument about whether we had breached anything.
>
> Second, the regression itself. A change made for EU compliance to an effective date had shifted US disbursement dates by a day. Reverting was the fast option. I argued for the robust one: a region conditional in the table function, so EU and US keep independent semantics. The group chose it. The fix was deployed by two teammates and the incident closed in three days.

</details>
