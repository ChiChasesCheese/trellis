---
id: nr-amz-r3-senior-3
node: amazon.followups
type: qa
step: 74
---
## Q
<p class="title">Aiki 消费者 App<span class="meta">03 senior 追问</span></p>

*"With Core Data and CloudKit, what happens when the same card is edited on two devices, and how do you design for it?"*

## A
<span class="label">面试官在探</span> 面试官在探：你是否理解离线优先加同步系统里的一致性取舍

<span class="label">回答框架</span>

- 先说问题：两端离线修改同一数据，合并时会冲突
- 再说策略：按字段做最后写入胜出，或者对学习进度这类数据用合并而不是覆盖
- 然后说取舍：简单的策略可能丢掉一方修改，要看数据的价值
- 最后说验证：用多设备的测试场景覆盖冲突路径

<span class="label">为什么这是最佳实践</span>

同步系统里冲突是常态而不是例外。选择什么合并策略取决于数据的价值：学习进度丢失会伤害用户信任，所以更值得做细粒度合并。我现在还需要用自己的话把这块讲清楚，这里是一个资深工程师会采用的思路。

<div class="sources"><b>表达 · business English</b><br>• <b><i>last-writer-wins</i></b> — 最后写入者胜出<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Last-writer-wins is simple, but it can silently drop a user&#x27;s progress.”</span><br>• <b><i>eventual consistency</i></b> — 最终一致性<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Sync across devices is eventually consistent, so the design has to expect conflicts.”</span></div>
