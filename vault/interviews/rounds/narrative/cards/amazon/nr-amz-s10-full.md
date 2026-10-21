---
id: nr-amz-s10-full
node: amazon.full
type: qa
step: 10
---
## Q
<p class="title">退款费 billing-terms 复盘<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：一家大型电商商户切到 net settlement 后，部分退款费仍带着旧的 monthly billing terms。我 own 爆炸半径的估算和根因，补救范围必须按正确的数字来定。
- 问题：我写的第一版查询给出约 196K 行、61 个商户、约 11,123 美元。但在任何人据此行动之前，我重读自己的谓词，发现它没有检查新的定价计划在费用创建时是否已经存在。很多计划是几个月后才回填的，写入当时其实是对的。
- 我做了什么：我加上 ps_curr.created_at <= bf.created_at 重跑，真实范围是 21,923 行、10,330 个 credits、30 个商户、5,854.52 美元。根因是退款费路径复制了 credit 的历史 pricing_schedule_id，而没有在费用创建时重新解析生效计划。顺带发现上游一个脆弱点：计划在交易流给当天 credit 盖章之后 1 小时 32 分才写入。
- 结果：范围从 200K 行、60 个商户缩到约 22K 行、30 个商户、不到 6,000 美元。一个修法（费用创建时解析生效计划）同时覆盖下游和上游两个脆弱点。
- 为什么这样做 / 学到：错的数字一旦进入补救计划，代价比公开撤回大得多，所以我宁可自己公开撤回。此后每个结论都配一条可重跑的查询，爆炸半径谓词必须检查时间有效性。

<span class="label">英文口述（60–90 秒）</span>

After a large e-commerce merchant moved to net settlement, some refund fees came out tagged with the old monthly billing terms. My first blast-radius query said about two hundred thousand fee rows across sixty merchants. Before anyone acted on it, I re-examined the predicate and found it was wrong: it didn't check that the new pricing schedule existed at the time the fee was created. Many of those rows had schedules backfilled months later and were correct when written. Adding that condition took the real scope to about twenty-two thousand rows, thirty merchants, under six thousand dollars. The root cause was that the refund-fee path copied the credit's historical pricing-schedule ID instead of resolving the effective schedule at fee-creation time. Along the way I found a second, upstream fragility: a schedule written to the database an hour and a half after the transaction stream had already stamped that day's credits. One fix covers both. I'd rather retract my own number in public than have a remediation sized off a bad predicate.

<div class="sources"><b>表达 · business English</b><br>• <b><i>retract a number</i></b> — 撤回自己报出的数字<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I retracted my own number before anyone built a plan on it.”</span><br>• <b><i>size the blast radius</i></b> — 估算影响范围<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I was asked to size the blast radius of the bad billing terms.”</span><br>• <b><i>root cause</i></b> — 根本原因<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The root cause was copying the credit&#x27;s historical schedule ID.”</span></div>
