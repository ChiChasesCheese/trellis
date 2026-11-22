---
id: aid-role-define-probe
node: t08.role-shift
type: qa
step: 2
tags: [考点]
---
## Q
**定义问题 · 改写需求**｜考点 · 必会

产品说："让搜索更快更准。"你要把它交给 agent 做。写出四个能让 agent 和审查者都能判断"做没做到"的条目。

## A
| 部分 | 内容 |
|---|---|
| 目标 | 常用查询的 p95 响应时间下降，前 10 条结果的命中不退步 |
| 验收标准 | 在固定的 1 万条查询样本上，p95 低于现有的 80%；离线评测集上的 top-10 命中率不低于现在 |
| 边界 | 空查询、超长查询、特殊字符、并发 |
| 范围外 | 不改排序模型；不改索引格式 |

**配套检查：** 基准脚本（跑样本、报 p95）和离线评测脚本；两个都是**可运行的 check**。

**别做：** 把"更快更准"原样交给 agent——它会按自己的理解选一个方向，你只能在 diff 里发现选错了。

**注意：** 80%、1 万条是例子数字，不是建议值。

**出处：** Claude Code docs《Best practices》（Brainstorm with Claude first；Give Claude a check to run）
