---
id: nr-amz-s2-senior-2
node: amazon.followups
type: qa
step: 8
---
## Q
<p class="title">Quality-check 框架<span class="meta">03 senior 追问</span></p>

*"How would you roll out the merchant-level change safely across all eight subject areas?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对灰度和回退是否有清晰的方法，而不是一次性全推。

<span class="label">回答框架</span>

- 先说顺序：已在一个 subject area 验证过，再按风险从低到高逐个改造
- 再说兼容：strictest wins 保证改造过和没改造的 procedure 混跑也是安全的
- 再说验证：新旧读结果在同一批数据上对比，差异必须能解释
- 最后说回退：每个 area 单独可退，退回就是今天的表级行为

<span class="label">为什么这是最佳实践</span>

strictest wins 让每个 subject area 可以独立迁移，混跑时最坏也只是退化成表级阻塞，所以不需要停机窗口或一次性切换。逐个迁移配合新旧结果对比，能在影响面最小时发现问题。这也是我把全框架铺开排在 net settlement 之后的原因，不让两件大事同时进行。

<div class="sources"><b>表达 · business English</b><br>• <b><i>incremental rollout</i></b> — 渐进式铺开<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I would do an incremental rollout, one subject area at a time, each independently reversible.”</span><br>• <b><i>backward compatible</i></b> — 向后兼容<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Strictest wins keeps the change backward compatible with unconverted procedures.”</span></div>
