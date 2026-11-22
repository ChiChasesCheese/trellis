---
id: aid-worktree-split
node: t02.session-git-worktree
type: qa
step: 2
tags: [实践]
---
## Q
**并行 session · 切分任务与合并**｜实践 · 必会

三个 session 分别改认证、支付、通知，都动了同一个 `config.ts`。你怎么切任务、怎么让合并不痛苦？

## A
| 做 | 为什么 |
|---|---|
| 按**文件边界**切任务，而不是按功能名切 | 冲突发生在文件，不在概念上 |
| 共享的文件（`config.ts`）先单独做一个提交并合并，各分支再基于它 | 消除三方同时改同一处 |
| 每个 worktree 一个分支，合并前各自跑完检查 | 合并时冲突的责任方清楚 |
| 每个 worktree 是新检出：被 gitignore 的文件（如 `.env`）和依赖不在 | 在 `.worktreeinclude` 里列出要复制的小文件；依赖安装命令写进 CLAUDE.md（项目说明文件，t03 讲） |

**别做：** 三个 agent 都"顺手"改共享文件，最后让第四个 agent 解冲突。

**清理（官方）：** 没改动的 worktree 退出时会被自动删除；`claude -p --worktree` 的要自己用 `git worktree remove` 清理。

**时效：** `.worktreeinclude` 是 Claude Code 当前的做法，其他工具各有各的约定；"每个 session 一个隔离目录"不变。

**出处：** Claude Code docs《Best practices》（Run sessions in parallel）
