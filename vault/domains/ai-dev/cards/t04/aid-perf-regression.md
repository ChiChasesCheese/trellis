---
id: aid-perf-regression
node: t04.performance-complexity-regression
type: qa
step: 1
tags: [摘要]
---
## Q
**Performance 与 complexity regression**｜摘要 · 追问

agent 重写了订单列表接口，功能测试全过，上线后接口变慢了。AI 代码常见的性能问题和排查办法？

## A
| 常见问题 | 例 | 排查 |
|---|---|---|
| **O(n²)** | 循环里在列表上 `in` 查找 | 用大数据量的基准跑；读循环嵌套 |
| **N+1 查询** | 循环里每条记录一次数据库查询 | 开 SQL 日志数查询条数；看 ORM 的预加载 |
| **多余的工作** | 重复解析、重复请求 | profile |
| **不必要的全量加载** | 把整表读进内存 | 查询计划（EXPLAIN）、内存用量 |

**为什么 AI 常犯：** 功能测试用的是几条样例数据；"能跑通"不要求高效，除非你给它一个性能判据。

**做：** 把性能写进 spec（"1 万条数据 p95 < 200ms"），给一个基准测试当 check；对数据库访问看查询计划。
**别做：** 只用 3 行 fixture 测性能相关代码。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Give Claude a check to run：可运行的 check 才是判据）

</details>
