---
id: nr-amz-s9-hook
node: amazon.outline
type: qa
step: 25
---
## Q
<p class="title">Amex 出款延迟事故<span class="meta">02 提纲</span></p>

开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
<span class="label">开场</span>

**A large marketplace merchant reported about four million dollars of Amex payouts "missing"; I was named one of three fix owners and separated expected latency from the real regression.**

<span class="label">适用 LP</span>

- 主：**Customer Obsession**
- 副：Dive Deep、Have Backbone、Earn Trust、Deliver Results、Ownership、Insist on the Highest Standards

<span class="label">数字</span>

- 商户报告 **~$4M** Amex 出款"不见了"（延迟，不是丢失）
- **三位 fix owner 之一**，由指挥点名
- **T+7** = 内部管线 SLA（美国 aggregated Amex）
- **6/23** 一次 Agg-Amex effective-date 改动（为 EU 合规）把 US 出款日推后 **~1 天**：真实根因
- 事故 **07-06 → 07-09** 关闭，**三天**

<div class="sources"><b>表达 · business English</b><br>• <b><i>on the hook</i></b> — 要负责、跑不掉<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“With four million dollars in question, the three of us were on the hook for the fix.”</span><br>• <b><i>close out an incident</i></b> — 把事故收尾关闭<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“We closed out the incident in three days.”</span><br>• <b><i>rule out</i></b> — 排除<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Stating the SLA let us rule out a breach before digging for the real cause.”</span></div>
