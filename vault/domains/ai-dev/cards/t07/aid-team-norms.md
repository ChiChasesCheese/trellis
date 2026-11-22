---
id: aid-team-norms
node: t07.context-file-review-rules-disclosure
type: qa
step: 1
tags: [实践]
---
## Q
**团队规范**｜实践 · 追问

团队里个人用 AI 的做法差异很大，有人做得很好。怎么把个人技巧变成共享资产？

## A
| 资产 | 内容 | 放哪 |
|---|---|---|
| **context file** | 命令、约定、坑 | 仓库 `CLAUDE.md` / `AGENTS.md`，改动走 PR |
| **review rules** | AI 参与的 PR 怎么审：体量上限、先看测试改动、对照 spec | 贡献指南或 PR 模板 |
| **disclosure 约定** | 要不要在 PR 里说明 AI 参与了什么；责任仍归提交者 | PR 模板一栏 |
| **权限配置** | 共享的 allow / ask / deny | 提交进版本控制；用 managed settings 统一下发 |
| **流程封装** | 发布、迁移、审查 | skill，团队仓库 |

**官方团队建议：** 用 managed settings 统一组织标准；通过版本控制共享已批准的权限配置；培训成员；用 OpenTelemetry 指标监控使用。

**做：** 每个新坑（agent 一再犯的错）改一次 CLAUDE.md，提 PR，写明原因。
**别做：** 每人一份私人 prompt 合集，从不共享。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Security》（Team security）；《Best practices》（Keep CLAUDE.md short）

</details>
