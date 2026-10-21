---
id: nr-amz-g3-senior-1
node: amazon.followups
type: qa
step: 87
---
## Q
<p class="title">GenAI 不必要的时候<span class="meta">03 senior 追问</span></p>

*"How do you decide, in the moment, whether a task is worth delegating to an agent?"*

## A
<span class="label">面试官在探</span> 面试官在探：你有没有可复用的判断框架，而不是凭感觉。

<span class="label">回答框架</span>

- 先问答案是否确定：确定则用脚本
- 再问改动大小：一行就地改，实质改动回到同一个有上下文的代理
- 最后问有没有可执行的验收：没有就先写验收再委派

<span class="label">为什么这是最佳实践</span>

委派有成本，包括等待、上下文和审查。三个问题依次过滤，能把大多数不划算的委派挡在门外。先问最便宜的问题，决策本身也省时间。

<div class="sources"><b>表达 · business English</b><br>• <b><i>decision rule</i></b> — 判断规则<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I use a three-question decision rule before delegating.”</span><br>• <b><i>back-of-envelope</i></b> — 粗略估算<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A back-of-envelope cost check usually settles it.”</span></div>
