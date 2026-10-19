---
id: nr-amz-s1-relp
node: amazon.outline
type: qa
step: 3
---
## Q
<p class="title">Amex 结算管线<span class="meta">02 提纲</span></p>

换成别的 LP 问时，强调哪一段？

## A
- **Ownership**：stub → 设计 → 上线 → 18 个月 on-call；kill switch；EU 扩展不是别人派的；别说成「团队做的」
- **Deliver Results**：22M 笔、最大单 PR、可急停、EU 扩展；不说美元数字
- **Dive Deep**：迟到文件靠读 load history 而不是看板；拒付标志复合键
- **Insist on the Highest Standards**：if it breaks, it must record, never drop；三层正确性；别声称 "no bugs"
- **Invent and Simplify**：一个 flag 把 Amex 从其他卡组织路径分流，一条 UPDATE 急停；会改成配置表 + 通用解析
- **Frugality**：stream-has-data 检查避免空文件起 warehouse；没有成本数字，别编

<div class="sources"><b>表达 · business English</b><br>• <b><i>take end-to-end ownership</i></b> — 承担端到端责任<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Nobody assigned the EU extension to me; I took end-to-end ownership of it.”</span><br>• <b><i>raise the bar</i></b> — 抬高标准<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Three layers of correctness checks raised the bar for what we call a settled fee.”</span><br>• <b><i>trace it to the root</i></b> — 追到根因<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I traced the late-file problem to the root by reading the load history instead of a dashboard.”</span></div>
