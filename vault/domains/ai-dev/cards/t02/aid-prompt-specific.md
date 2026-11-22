---
id: aid-prompt-specific
node: t02.prompt-scope-constraints-references
type: qa
step: 1
tags: [摘要]
---
## Q
**写具体的 prompt**｜摘要 · 必会

"修一下登录 bug"和下面这条，agent 的表现为什么差很多？

> users report login fails after the session times out. look at token refresh in src/auth/, write a failing test that reproduces it, then fix it

## A
**第二条给了 agent 读代码读不出来的信息：** 症状、范围、"修好"的判据。

| 要素 | 例 | 缺了会怎样 |
|---|---|---|
| **scope** | token refresh in src/auth/ | 它在全仓库乱找，可能改错地方 |
| **constraints** | no new libraries | 引入你不想要的依赖 |
| **references** | follow the pattern in HotDogWidget.php | 另起风格，和现有代码不一致 |
| **done criterion** | write a failing test, then fix | 没法判断是否真的修好 |

**把已有的东西直接给它：** 文件（`@路径` 引入内容）、截图、命令输出（`cat error.log | claude -p "…"`）。比描述快，也更准。

**模糊的代价：** 模糊提示换来过度实现或做错方向；官方还提到 agent 倾向按最保守的字面理解做最小的事，想要更完整的版本要明说（例如"边界状态、保存流程、键盘操作都要做，不只是布局"）。

**出处：** Claude Code docs《Best practices》（Write a specific prompt）
