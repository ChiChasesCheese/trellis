---
id: aid-epic-loop-probe
node: t02.explore-plan-implement-commit
type: qa
step: 2
tags: [考点]
---
## Q
**四段循环 · 计划里查什么**｜考点 · 必会

agent 交来的限流计划是："新建 RateLimiter 类，在所有路由前加中间件，用内存计数。"你批准之前该问哪三个问题？

## A
| 问题 | 为什么要问 | 这份计划里的洞 |
|---|---|---|
| 它读过现有的中间件和配置吗？ | 防止重新发明一个和现有模式不一致的东西 | 没提到任何现有文件 |
| 状态放哪？ | 部署多个实例时，内存计数各算各的，限流形同虚设 | "内存计数"在多实例下不成立 |
| 怎么验证？ | 没有检查，"做完了"没法判定 | 没有测试，没有验证步骤 |

**做：** 在计划阶段把这三条指出来，让它改计划，再批准。
**别做：** 看着"合理"就让它开始实现，然后在 800 行 diff 里找问题。

**追问：** 计划本身要不要存下来？要。写成文件（如 SPEC.md），之后可以在**新 session** 里照着它实现，也可以拿它当审查标准。见下一叶。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Best practices》（Brainstorm with Claude first）；《How Claude Code works》（Plan mode）

</details>
