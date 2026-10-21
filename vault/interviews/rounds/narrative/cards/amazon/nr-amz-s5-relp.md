---
id: nr-amz-s5-relp
node: amazon.outline
type: qa
step: 15
---
## Q
<p class="title">Net Settlement 数据源切换<span class="meta">02 提纲</span></p>

换成别的 LP 问时，强调哪一段？

## A
- **Ownership**：费用侧最硬的一块；toggle 灰度；窗口化的 ON 风险写在注释里；别说「唯一 owner」
- **Deliver Results**：数字链 99.9% / 0.224% / 13.7M；模板被复用；不说「零回归」「merchant by merchant」「两周」
- **Are Right, A Lot**：先 discovery 再动手，用数据 disconfirm 自己；讲选 B 的理由
- **Dive Deep**：0.07% 全是时序，0.224% 必须解释；两个可解释差异；别混用两个百分比
- **Insist on the Highest Standards**："Deploy is not release."：toggle 默认关、预生产先放、互补 task 防双计
- **Invent and Simplify**：用静态拆分替换有状态 fallback，去掉运行时判断
- **Bias for Action**：暗发布 = 默认关 + 可回退，所以能在生产完全证明前行动；别夸大成「冒险」
- **Customer Obsession**：费用赶不上净额窗口会影响商户出款金额；未验证的因果别说死
- **Think Big**：这是一个涉及数百亿交易量项目的前置；别把 $55B 说成我的产出
- **Frugality**：一个月窗口让扫描成本在只增不减的表上保持恒定（zone-map 剪枝）

<div class="sources"><b>表达 · business English</b><br>• <b><i>disconfirm yourself</i></b> — 主动找证据推翻自己的判断<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I ran the full outer join to try to disconfirm my own assumption that the views matched.”</span><br>• <b><i>reversible</i></b> — 可回退的<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Because the toggle made the change reversible, I could act before production was fully proven.”</span><br>• <b><i>reusable template</i></b> — 可复用的模板<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The backfill SQL became a reusable template for the team&#x27;s CDC backfills.”</span></div>
