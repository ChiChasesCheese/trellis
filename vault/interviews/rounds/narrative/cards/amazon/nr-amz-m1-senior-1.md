---
id: nr-amz-m1-senior-1
node: amazon.followups
type: qa
step: 57
---
## Q
<p class="title">新人 onboarding 与带教<span class="meta">03 senior 追问</span></p>

*"How do you give a new engineer difficult feedback on a design that plugs into your platform?"*

## A
<span class="label">面试官在探</span> 面试官在探：你给反馈的方法，既保标准又保关系。

<span class="label">回答框架</span>

- 先讲契约和下游约束，而不是品评个人：边界、键语义、重试行为
- 用具体场景提问，例如同一事件被重复投递时会怎样
- 区分必须改的（正确性）与可以讨论的（偏好）
- 给出理由并留出对方反驳的空间，必要时改变自己的想法

<span class="label">为什么这是最佳实践</span>

用下游如何消费作为评审的锚点，反馈就是关于系统事实的，而不是关于人的判断，对方更容易接受也更容易学会这种思考方式。把必须改和可商量分开，避免所有意见都被当作命令。我在这个故事里没有可举证的具体反馈场景，这里说的是我会采用的方法。

<div class="sources"><b>表达 · business English</b><br>• <b><i>critique the work, not the person</i></b> — 对事不对人<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I critique the design, not the person, anchored on how events are consumed.”</span><br>• <b><i>non-negotiable</i></b> — 没有商量余地的底线<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Correctness at the seam is non-negotiable; style is up for discussion.”</span></div>
