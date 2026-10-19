---
id: nr-amz-tech-why-migrate
node: amazon.tech
type: qa
step: 9
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

为什么要把 Kotlin / Ruby 的费用逻辑迁到 Snowflake？真实原因怎么讲？

## A
<span class="label">有依据的原因</span> （来自你的管线经历）**数据局部性**：交易和费用数据本来就在 Snowflake，服务要先把数据搬出来、算完再写回；**事务性 `MERGE`** 让每一步可重复执行而不重复计费；**空输入不启动 warehouse**（stream 没有新数据就跳过），只为真正有数据的运行付费。

常见的其他原因（挑你能证实的说，不确定的不要当成事实讲）｜
- 少一组要部署、扩容、值班的服务（fewer moving parts）
- 财务逻辑用 SQL 写，财务和数据团队能读、能审计
- 批量逻辑写成集合运算，比逐行循环快一个量级
- Ruby 维护者变少，平台向少数技术栈收敛

<span class="label">怎么讲</span> 先讲问题（数据来回搬、重复计费风险、运维成本），再讲选择，最后讲代价和你怎么补（下一张卡）。*"The logic was batch and set-based, and the data already lived in Snowflake, so keeping it in a Ruby service meant shipping data back and forth for no benefit."*

<div class="sources"><b>表达 · business English</b><br>• <b><i>the business case</i></b> — 这件事的商业理由<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The business case was fewer services to run and fees you could audit in SQL.”</span><br>• <b><i>consolidate the stack</i></b> — 收敛技术栈<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“We were consolidating the stack, and Ruby was the odd one out.”</span><br>• <b><i>behavioral parity</i></b> — 行为一致（迁移前后结果完全相同）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Nothing shipped until we had behavioral parity on every fee type.”</span></div>
