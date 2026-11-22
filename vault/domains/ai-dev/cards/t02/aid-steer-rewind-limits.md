---
id: aid-steer-rewind-limits
node: t02.interrupt-rollback-session
type: qa
step: 2
tags: [考点]
---
## Q
**Rewind 的边界**｜考点 · 追问

agent 跑了一个脚本，改了 20 个文件还写了一次数据库。你 `/rewind` 之后，哪些恢复了、哪些没有？

## A
| 内容 | 能还原吗 | 原因 |
|---|---|---|
| agent 用文件编辑工具改的文件 | 能 | rewind 前有快照 |
| 只被脚本（Bash 命令）改动的文件 | **不能** | 不在快照范围内 |
| 符号链接、硬链接的文件 | 不还原 | 官方文档的限制 |
| 数据库写入、API 调用、部署 | **不能** | 远程动作无法快照 |

**结论：** rewind 是文件编辑的撤销键，不是世界的撤销键。风险动作要靠**权限规则**提前拦住（见 t03、t06），代码改动靠 **git** 兜底。

**做：** 让 agent 动手前工作区干净、改动在分支上；会写库的任务先在沙箱或副本上跑。

**出处：** Claude Code docs《How Claude Code works》（Undo changes with checkpoints）；《Best practices》（Steer the session）
