---
id: aid-ctxfile-what
node: t03.context-file-claude-md-agents-md
type: qa
step: 1
tags: [摘要]
---
## Q
**项目 context file · CLAUDE.md / AGENTS.md**｜摘要 · 必会

每次开新 session，agent 都不记得上次的事。怎么让它一开始就知道"这个项目怎么跑测试、什么不能碰"？

## A
**context file＝放在仓库里、每次 session 开始自动读进 context 的 markdown 说明文件。** Claude Code 读 `CLAUDE.md`，很多其他工具读 `AGENTS.md`（见非核心叶）。

**每个 session 都会加载，所以每一行都在占 agent 每一次任务的注意力。** 只放两类东西：

| 放 | 例 |
|---|---|
| 怎么确认工作做对了 | 确切的测试、type check、lint 命令；怎么只跑一个测试文件 |
| 读代码读不出来的东西 | 老代码里一个到处都是、但新代码不许学的模式；看起来没用其实有用的目录；团队在会上定的决定；集成测试需要的环境变量 |

**删掉：** agent 读仓库就能找到的（文件结构、框架、已有约定）。

**判断一行去留的两问：** ① 它读代码能找到吗？② 它真的会去找吗？两个都"是"，就删。

```markdown
# Commands
- Run one test file: pnpm vitest run path/to/file.test.ts
- Typecheck: pnpm tsc --noEmit

# Gotchas
- src/legacy/ is still live but don't copy its patterns into new code
- Integration tests need DATABASE_URL set, see .env.example
```

**起步：** `/init` 从代码库生成初稿，之后的工作主要是删行。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Keep CLAUDE.md short）；《How Claude remembers your project》

</details>
