---
id: nr-amz-r2-senior-1
node: amazon.followups
type: qa
step: 67
---
## Q
<p class="title">AI-native 迁移<span class="meta">03 senior 追问</span></p>

*"How did you establish that the Snowflake and Java version really behaved like the Ruby and Kotlin version?"*

## A
<span class="label">面试官在探</span> 面试官在探：你对 parity 的验证方法是否系统，而不只是看起来对

<span class="label">回答框架</span>

- 先说基线：先用测试把旧系统的现有行为固定下来，作为可执行的规格
- 再说对照：新旧实现用同一批输入对比输出，尤其是边界和金额舍入
- 然后说差异处理：每个差异要么是旧系统 bug 要么是迁移错误，必须有人裁决
- 最后说上线保护：影子运行或灰度，加上监控阈值

<span class="label">为什么这是最佳实践</span>

旧代码往往藏着没有文档的行为，只有先把它变成测试，parity 才有可衡量的定义。新旧同输入对拍能把差异暴露出来，再逐个裁决，避免把 bug 也迁过去。这是我会采用的验证路径，具体通过率没有精确数字，所以不夸大。

<div class="sources"><b>表达 · business English</b><br>• <b><i>executable spec</i></b> — 可执行的规格（测试即规格）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The tests are the executable spec of what the legacy code actually does.”</span><br>• <b><i>differential testing</i></b> — 差分测试，新旧同输入比输出<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Differential testing on the same inputs shows exactly where the two versions diverge.”</span></div>
