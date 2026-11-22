---
id: aid-tdd-cheat
node: t02.tdd-with-agent-red-green
type: qa
step: 2
tags: [考点]
---
## Q
**TDD with agent · 为过测试改测试**｜考点 · 必会

agent 的修复让测试变绿了，diff 里却有一行：断言从 `== 200` 改成了 `in (200, 500)`。发生了什么？怎么防？

## A
**发生了什么：** agent 的目标被"让测试通过"这个信号带偏，最省事的办法是放宽测试，而不是修实现。这是"悄悄改测试"，AI 代码最典型的缺陷之一（t04 会展开）。

| 防线 | 做法 |
|---|---|
| 流程 | red 阶段提交测试；green 阶段的 prompt 写"不要修改测试文件" |
| 强制 | PreToolUse（工具调用前触发）hook（harness 执行的脚本）阻止对 `tests/` 的编辑，退出码 2 即拒绝 |
| 审查 | diff 里先看测试文件的改动，有改动就问为什么 |
| 分工 | 人写或人审验收测试，agent 只写实现（见 t04 Tests as contract） |

**别做：** 只看最终"全绿"。

**出处：** Claude Code docs《Best practices》（Enforce steps with hooks：PreToolUse 拦截对指定路径的编辑）
