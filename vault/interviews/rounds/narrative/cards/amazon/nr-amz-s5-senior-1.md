---
id: nr-amz-s5-senior-1
node: amazon.followups
type: qa
step: 22
---
## Q
<p class="title">Net Settlement 数据源切换<span class="meta">03 senior 追问</span></p>

*"How did you decide that 0.224 percent was acceptable, and what would have made you hold the switch?"*

## A
<span class="label">面试官在探</span> 面试官在探：你上线前有没有预先定义“通过/不通过”的标准，而不是看到数字再合理化。

<span class="label">回答框架</span>

- 先说差异的性质：是记录数差异，不是金额或字段冲突，并且可以拆解归类
- 再说门槛应该在跑之前定：按类别解释全部差异，任何解释不了的差异就是 no-go
- 说明我当时的判断是 0.224% 可接受，没有预设的数字门槛，下次会先写下来
- 最后说放量也留了退路：toggle 默认关，可以随时回退

<span class="label">为什么这是最佳实践</span>

好的验证是先写下通过标准再看数据，这样结论不会被结果牵着走。我的做法是把差异拆成可解释的类别；如果有无法解释的残差，我会不放量。事后诚实说明当时没有预设阈值，反而比编一个阈值更可信，而且能顺势讲出下次的改进：先写门槛，再跑查询。

<div class="sources"><b>表达 · business English</b><br>• <b><i>go/no-go criteria</i></b> — 放行/不放行的判定标准<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Next time I would write the go/no-go criteria down before running the comparison.”</span><br>• <b><i>unexplained residual</i></b> — 无法解释的残差<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Any unexplained residual in the difference would have been a reason to hold the switch.”</span></div>
