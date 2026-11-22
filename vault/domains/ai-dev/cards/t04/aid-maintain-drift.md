---
id: aid-maintain-drift
node: t04.maintainability-duplication-style-drift-consiste
type: qa
step: 1
tags: [摘要]
---
## Q
**Maintainability · 重复与风格漂移**｜摘要 · 追问

半年后你发现代码库里有 5 个几乎一样的"重试"函数，各用各的风格。为什么 agent 会产生这种东西？怎么约束？

## A
**成因：** 每个 session 的 context 里只有当时读到的代码；它可能没看到已有的实现，就再写一个（duplication）；不同 session 的风格各不相同（style drift）。

| 约束 | 机制 |
|---|---|
| prompt 里指向现有模式 | "follow the pattern in X"，让它复用而不是新建 |
| CLAUDE.md 写"不要学的老模式"和"统一用哪个 helper" | 每次 session 都知道 |
| linter、formatter | 机械地统一风格；用 hook 在每次编辑后自动跑 |
| 架构测试 | 把"某层不能依赖某层"写成测试，违反就红 |
| 审查时问"仓库里已经有类似的吗" | 人把关复用 |

**官方例子：** "团队约定用哪个错误处理 helper"属于该写进 CLAUDE.md 的东西；PostToolUse hook 在每次编辑后跑 prettier。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Keep CLAUDE.md short；Enforce steps with hooks）

</details>
