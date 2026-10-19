---
id: nr-amz-s5-senior-2
node: amazon.followups
type: qa
step: 23
---
## Q
<p class="title">Net Settlement 数据源切换<span class="meta">03 senior 追问</span></p>

*"How would you know in production that the switch is actually working, after the toggle is on?"*

## A
<span class="label">面试官在探</span> 面试官在探：你上线后有没有持续的观测与告警，而不是上线即结束。

<span class="label">回答框架</span>

- 先说业务信号：费用在净额窗口之前到齐的比例，以及出款金额是否按预期
- 再说数据信号：两个视图的行数差、迟到记录数、合成键重复数
- 对照基线：切换前后同一时间窗口的对比
- 最后说回退触发条件：超过阈值就关掉 toggle

<span class="label">为什么这是最佳实践</span>

切换的目的是让费用赶上窗口，所以最直接的验证是到齐率，而不是行数。再加上重复键检测，防止互斥假设失效造成双计。有了预先定义的触发条件，toggle 才真正等于安全网，而不只是开关。

<div class="sources"><b>表达 · business English</b><br>• <b><i>leading indicator</i></b> — 先行指标，问题爆发前就会变化<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The share of fees landing before the cutoff is the leading indicator that the switch works.”</span><br>• <b><i>rollback trigger</i></b> — 触发回退的条件<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I would define a rollback trigger, such as duplicate keys above zero, before flipping the toggle.”</span></div>
