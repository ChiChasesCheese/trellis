---
id: nr-amz-s3-senior-2
node: amazon.followups
type: qa
step: 13
---
## Q
<p class="title">ACH 费用 NULL 事故<span class="meta">03 senior 追问</span></p>

*"How do you make sure a silent-NULL class of bug is caught earlier next time, beyond this one fix?"*

## A
<span class="label">面试官在探</span> 面试官在探：你是在修一个 bug，还是在消灭一类 bug。

<span class="label">回答框架</span>

- 先说接缝：在边界处对不可映射的值显式报错，不让 NULL 往下传
- 再说设计：单一函数加默认参数，新分支选不到不完整的实现
- 再说测试：用真实形态的 fixture 跑完整链路，断言费用而不只是路由
- 最后说监控：保留这个每日健康检查，它正是发现问题的那道网

<span class="label">为什么这是最佳实践</span>

NULL 拼接静默得到 NULL 是 SQL 的属性，指望每个调用点都记得检查是不现实的，所以规则放在接缝上。让错误无法被选到，比提醒大家小心可靠得多。测试要用会触发该路径的数据，否则测试通过也说明不了什么。

<div class="sources"><b>表达 · business English</b><br>• <b><i>make illegal states unrepresentable</i></b> — 让非法状态无法被表达出来<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“One function with a default parameter makes the incomplete implementation impossible to pick.”</span><br>• <b><i>defense at the seam</i></b> — 在接缝处设防<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I put the rule at the seam, not at each call site.”</span></div>
