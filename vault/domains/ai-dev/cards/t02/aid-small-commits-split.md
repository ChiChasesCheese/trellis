---
id: aid-small-commits-split
node: t02.small-commits
type: qa
step: 2
tags: [实践]
---
## Q
**Small commits · 怎么拆**｜实践 · 追问

一个"把订单模块迁到新的错误处理"的大任务，怎么拆成每块都能审、能回退的提交？

## A
| 原则 | 做法 |
|---|---|
| 一个提交一个意图 | 先加新错误类型（纯新增），再逐个调用点迁移，最后删旧的 |
| 每个提交单独能过检查 | 每次提交前跑测试和 type check；失败的不提交 |
| 机械改动和行为改动分开 | 全量改名一个提交，逻辑修改另一个，审查时读起来完全不同 |
| 顺序可逆 | 越到后面越是删除，出问题时只回退最后一块 |

**让 agent 配合的方式：** 在 prompt 里写明"每迁完一个子模块就提交一次，提交前跑 `pnpm test orders`"；或把迁移做成可批量、按文件重复的脚本，每个文件一个提交。

**别做：** 做完所有工作再一个"wip"大提交——要审的人只能读 2000 行 diff（见 t04 small-diff review）。

**出处：** Claude Code docs《Best practices》（Run sessions in parallel：/batch 把大改拆成单元，各自一个独立工作目录和 PR）
