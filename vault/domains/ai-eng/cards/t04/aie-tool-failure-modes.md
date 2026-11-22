---
id: aie-tool-failure-modes
node: t04.tool-design-agent-computer-interface
type: qa
step: 2
tags: [考点]
---
## Q
**Tool design · tool 调用常见的三种错**｜考点 · 必会

agent 调用 `lbs_to_kg`（只有一个参数 `lbs`）。下面三次调用分别错在哪？tool 设计上怎么减少这类错？

1. 调用了 `bing_search`，但 inventory 里没有这个 tool；
2. 调用 `lbs_to_kg(lbs=100, unit="kg")`；
3. 调用 `lbs_to_kg(lbs=100)`，但用户给的是 120 磅。

## A
| 调用 | 错误类型 | 好发现吗 |
|---|---|---|
| 1 | **Invalid tool**：不存在的 tool | 容易，对照 inventory 即可 |
| 2 | **Valid tool, invalid parameters**：参数不合法 | 容易，用参数 schema 校验 |
| 3 | **Valid tool, incorrect parameter values**：值不对 | **最难**，形式完全合法 |

**设计上的对策：**
- 第 1、2 类：有的 function calling API 能保证只生成合法的 tool，但**保证不了参数值正确**。服务端对 name、参数做 schema 校验，非法调用当错误返回给模型。
- 第 3 类：让系统**报告每次调用用了什么参数值并检查**（书里的 Tip）；对高风险的 tool 要求确认。
- 防呆：参数设计让错误更难发生（如必须传绝对路径，枚举代替自由文本）。
- 工具太多也会让模型难以选择，通过实验确定合适的 tool 集合；某个 tool 模型总用错，先改描述和示例，实在不行就**换成一个更容易用的 tool**。

**测评方法：** 建一个 planning 数据集（任务，tool inventory），让 agent 对每个任务生成多个计划，统计：计划有效比例、tool 调用有效比例、调用了无效 tool 的频率、参数无效频率、参数值错误频率，再看哪类任务、哪个 tool 最常出错。

<details class="pt" markdown="1"><summary>出处</summary>

Huyen《AI Engineering》ch6 §Agent Failure Modes and Evaluation → Planning failures；§Function calling（Tip）

</details>
