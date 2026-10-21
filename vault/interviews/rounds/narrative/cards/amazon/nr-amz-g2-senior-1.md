---
id: nr-amz-g2-senior-1
node: amazon.followups
type: qa
step: 82
---
## Q
<p class="title">不依赖 agent 自述的正确性<span class="meta">03 senior 追问</span></p>

*"What stops the gate itself from becoming the thing agents optimize for, instead of real quality?"*

## A
<span class="label">面试官在探</span> 面试官在探：你是否意识到指标会被优化而偏离目标（Goodhart 问题）。

<span class="label">回答框架</span>

- 先承认风险：代理会为了通过验收而写出刚好满足格式的内容
- 再说对策：验收只管形状，实质由我读，并且我先读代理自己列的最弱论断
- 最后说独立路径：用第二条不同方法得到同一个答案来交叉验证

<span class="label">为什么这是最佳实践</span>

任何自动检查都只覆盖它被设计覆盖的维度，被优化的对象最终会钻空子。所以闸门要和人工审读、独立路径对拍配合使用，闸门管便宜的、人管贵的。

<div class="sources"><b>表达 · business English</b><br>• <b><i>game the metric</i></b> — 钻指标的空子<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Agents can game the metric, so the gate is never the whole review.”</span><br>• <b><i>defense in depth</i></b> — 纵深防御<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I use defense in depth: gate, reading and independent paths.”</span></div>
