---
id: nr-amz-s2-relp
node: amazon.outline
type: qa
step: 6
---
## Q
<p class="title">Quality-check 框架<span class="meta">02 提纲</span></p>

换成别的 LP 问时，强调哪一段？

## A
- **Invent and Simplify**：加校验从 "write a task, review, deploy" 变成 "insert a row"；别把 ADR 状态说成已上线
- **Insist on the Highest Standards**：下游不读半验证数据，做成 join 条件；讲 trigger-status 握手和 strictest-wins
- **Earn Trust**：自己发现并写 ADR 批评自己的设计；四方案否决理由外化；别夸大成「大家夸我」
- **Frugality**：只存失败行，最坏每月 ~800K 行而不是每天 2.4M；复用现有结果表、零新基础设施
- **Are Right, A Lot**：把自己的抽象当别人的代码一样 disconfirm；strictest wins 的正确性论证
- **Have Backbone**：对自己设计的反对；被追问时诚实说这不是与他人的分歧
- **Think Big**：不是 feature，是别人往上接的平台；8 次铺开、下游消费
- **Hire and Develop**：标准通过框架/ADR/onboarding doc 传递；没有 code-review 痕迹，别声称

<div class="sources"><b>表达 · business English</b><br>• <b><i>disconfirm my own assumptions</i></b> — 主动去证伪自己的假设<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I tried to disconfirm my own abstraction the way I would review someone else&#x27;s code.”</span><br>• <b><i>build a platform, not a feature</i></b> — 做平台而不是单个功能<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I built a platform, not a feature, so other teams could plug checks in.”</span><br>• <b><i>be transparent about status</i></b> — 如实说明当前状态<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I stay transparent about status: the ADR direction is proven in one area, not rolled out everywhere.”</span></div>
