---
id: aid-cost-probe
node: t07.token-budget-model-tiering-subagent-cost
type: qa
step: 2
tags: [考点]
---
## Q
**成本 · 找出最大的一笔**｜考点 · 追问

某工程师的用量是同事的 6 倍。`/usage` 显示：一个 session 开了三天、做了五件不相关的事；还有两个后台 `/loop` 在每 15 分钟检查 CI。先动哪里？

## A
| 现象 | 成本机制 | 处理 |
|---|---|---|
| 一个 session 五件事 | 每轮重发全部历史；缓存过期后全价 | 任务间 `/clear`；用 `/rename` 保存要回来的 session |
| 后台 `/loop` | 每次都是同一 session 里的一轮，持续累积 | 不要在长对话里放着；换成只在 CI 红时触发的任务 |
| 大量 subagent（独立 context 里干活的 agent） | 每个单独计费 | 简单的用小模型；只留有收益的 |

**顺序：** 先处理"长 session"（影响每一轮），再处理后台循环（持续固定开销），最后才调模型档位。

**别做：** 直接给所有人降档——会损失关键任务的质量。

**出处：** Claude Code docs《Best practices》（Keep cost and context down：/clear、/loop 提醒）
