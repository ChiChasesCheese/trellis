---
id: src-pyramid-or-trophy
node: t07.test-strategy
type: qa
step: 2
tags: [追问]
---
## Q
**Test strategy · 金字塔还是奖杯**｜追问 · 追问

面试官追问："测试金字塔和测试奖杯，你更认同哪个？在你的后端项目里怎么选？"

## A
**一句话：** 都不是答案，是思考工具；按你的系统形态选，并根据 bug 的出处调整。

| | 更适合 |
|---|---|
| 金字塔 | 几乎没有界面的后端系统，部分原生移动应用（端到端和集成测试很难做） |
| 奖杯 | 前端；也越来越适合全栈应用，因为模块化后很多 bug 出在组件之间 |

**怎么做：** 看你的故障和 bug：多出在单个函数里，还是出在组件之间？多在组件之间就多写集成测试。

<details class="pt" markdown="1"><summary>面试官看什么 · 配哪类故事 · 出处</summary>

**面试官在考什么：** 你有没有主见，并能把选择讲成对系统的判断。

**出处：** Orosz《The Software Engineer's Guidebook》ch14 §4（The testing pyramid；The testing trophy）

</details>
