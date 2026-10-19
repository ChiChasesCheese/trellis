---
id: nr-amz-g2-senior-2
node: amazon.followups
type: qa
step: 83
---
## Q
<p class="title">不依赖 agent 自述的正确性<span class="meta">03 senior 追问</span></p>

*"How would you decide how many mutants are enough, and when to stop?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对测试充分性有没有成本意识，而不是追求数字。

<span class="label">回答框架</span>

- 先说变异应由真实风险驱动：从最容易写错的逻辑和历史上出过错的地方入手
- 再说停止条件：新增变异不再暴露新的测试缺口，边际收益下降
- 最后说成本：自动化变异工具能规模化，手写变异适合关键路径

<span class="label">为什么这是最佳实践</span>

变异得分是手段，不是目标。把力气放在高风险逻辑上，看到边际收益下降就停，这样既抓到真缺口又不把时间耗在凑数上。

<div class="sources"><b>表达 · business English</b><br>• <b><i>diminishing returns</i></b> — 边际收益递减<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I stop when new mutants show diminishing returns.”</span><br>• <b><i>risk-driven</i></b> — 由风险驱动<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I keep mutation risk-driven and focus on the logic that breaks most easily.”</span></div>
