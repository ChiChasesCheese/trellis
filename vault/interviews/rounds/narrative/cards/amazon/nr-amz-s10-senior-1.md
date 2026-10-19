---
id: nr-amz-s10-senior-1
node: amazon.followups
type: qa
step: 47
---
## Q
<p class="title">退款费 billing-terms 复盘<span class="meta">03 senior 追问</span></p>

*"How did you first realize the predicate was wrong, and how would you build that check into the process?"*

## A
<span class="label">面试官在探</span> 面试官在探：你的自我纠错是偶然还是有方法，能不能变成团队习惯。

<span class="label">回答框架</span>

- 触发点：数字看起来偏大，于是回头逐个条件问“这个条件在行创建那一刻成立吗”
- 具体检查：抽样几行，看计划是什么时候写入的
- 制度化：爆炸半径查询必须带时间有效性条件，并附一条可重跑的 SQL
- 让另一个人独立复核同一个谓词

<span class="label">为什么这是最佳实践</span>

估算类数字最容易错在“现在的状态”被误当成“当时的状态”。把谓词当作要证伪的假设，抽样核对时间线，就能抓住这类错误。把它写成模板或检查清单，才能让这个纠错不依赖某个人的警觉。具体我当时如何触发、是否已有清单，需要以实际情况为准。

<div class="sources"><b>表达 · business English</b><br>• <b><i>treat it as a hypothesis</i></b> — 当作待证伪的假设<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I treated my own query as a hypothesis to disprove.”</span><br>• <b><i>point-in-time correctness</i></b> — 按时间点的正确性<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The fix was about point-in-time correctness, not current state.”</span></div>
