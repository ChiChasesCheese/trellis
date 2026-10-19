---
id: nr-amz-s2-hook
node: amazon.outline
type: qa
step: 4
---
## Q
<p class="title">Quality-check 框架<span class="meta">02 提纲</span></p>

开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
<span class="label">开场</span>

**I replaced hand-written validation tasks with a config-driven quality gate, then wrote the ADR that overturned the granularity of my own design.**

<span class="label">适用 LP</span>

- 主：**Invent and Simplify**、**Insist on the Highest Standards**、**Earn Trust**、**Frugality**
- 副：Are Right A Lot、Have Backbone、Think Big、Hire and Develop

<span class="label">数字</span>

- 框架 PR **~1,500 行**
- 铺开 **8 个 subject area**，各 200–800 行，我自己铺
- **~50 个**持续失败商户（~4%）挡住 **35,000** 个商户
- **96.4%** 的检查一次通过，所以只存失败行
- 极端每月 **~80 万行**失败行，对比每商户每次一行 = 每天 **240 万行**
- 方案 D 的先例：TRANSFERS 区域已跑 **16 个月**
- 状态口径必须背："The framework and eight rollouts are live; merchant-level readiness is designed, reviewed, and proven for one subject area, and the framework-wide rollout is sequenced behind the net-settlement ramp." 不说「已改成商户级」

<div class="sources"><b>表达 · business English</b><br>• <b><i>at scale</i></b> — 到了规模上才暴露<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The granularity flaw only showed up at scale, with fifty bad merchants blocking thirty-five thousand.”</span><br>• <b><i>roughly four percent</i></b> — 大约百分之四<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Roughly four percent of merchants, about fifty, were blocking everyone else.”</span><br>• <b><i>worst case</i></b> — 最坏情况<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Storing only failures keeps the worst case around eight hundred thousand rows a month.”</span></div>
