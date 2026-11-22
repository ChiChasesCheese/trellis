---
id: aid-skills
node: t03.skills-slash-commands
type: qa
step: 1
tags: [实践]
---
## Q
**Skills 与 slash commands**｜实践 · 必会

团队的发布流程有七步，放进 CLAUDE.md 太长，不放 agent 又不会。怎么封装？

## A
**skill＝一个存成 `.claude/skills/<name>/SKILL.md` 的流程或团队知识。** 区别在加载时机：

| | CLAUDE.md | skill |
|---|---|---|
| 加载 | 每次 session 都进 context | 只有名字和描述常驻；任务需要时才读全文 |
| 适合 | 每个任务都用得到的 | 发布、迁移、审查等特定流程 |

**slash command＝你手动输入 `/名字` 来触发的命令。** 有副作用的流程（发布）加 `disable-model-invocation: true`，agent 就不会自己启动它，只有你敲 `/release` 才跑。

```markdown
---
name: release
description: Cut a new release: bump version, changelog, tag.
disable-model-invocation: true
---
1. Make sure you're on main with a clean tree. If not, stop and ask.
2. Run `pnpm changeset version` and commit.
3. Tag `v<new version>` and push the tag. CI publishes from there.
```

**规则同 CLAUDE.md：** 只写 agent 找不到的东西。

**安全：** 第三方 skill 是会被读进 context 当指令的文字，装之前先读（t06 供应链）。

**时效（2026-11）：** 文件位置和 frontmatter 字段是 Claude Code 的约定；封装"按需加载的流程说明"这个思路各工具都有。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Put team procedures in skills）；《How Claude Code works》（Manage context with skills and subagents）

</details>
