---
id: nr-amz-r2-senior-2
node: amazon.followups
type: qa
step: 68
---
## Q
<p class="title">AI-native 迁移<span class="meta">03 senior 追问</span></p>

*"What is the failure mode of AI-generated tests, and how do you defend against it?"*

## A
<span class="label">面试官在探</span> 面试官在探：你是否意识到让 AI 同时写代码和测试会产生相关性错误

<span class="label">回答框架</span>

- 先点出风险：同一个模型写代码和测试，会共享同样的误解，测试只是在复述实现
- 再说防御：测试的期望值来源于旧系统的真实行为或业务规则，而不是新代码
- 然后说人的角色：money code 我读每个 diff，并重点看断言是否有意义
- 最后说信号：看覆盖的边界与变异后是否还能发现错误

<span class="label">为什么这是最佳实践</span>

测试只有在独立于实现时才有价值。把期望值锚定在旧系统的真实输出和业务规则上，再由人审阅断言，才能防止 agent 写出永远通过的测试。这是 agent 提议、测试裁决能成立的前提。

<div class="sources"><b>表达 · business English</b><br>• <b><i>tautological test</i></b> — 同义反复的测试，永远通过<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The risk is a tautological test that just restates the implementation.”</span><br>• <b><i>correlated errors</i></b> — 相关性错误，同源误解一起出错<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“If one model writes both code and tests, you get correlated errors.”</span></div>
