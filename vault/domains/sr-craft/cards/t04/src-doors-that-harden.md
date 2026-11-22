---
id: src-doors-that-harden
node: t04.one-way-vs-two-way-doors
type: qa
step: 2
tags: [追问]
---
## Q
**Two-way doors that become one-way**｜考点 · 追问

面试官追问："你说先选个简单方案，以后不行再换。哪些决定在做的时候看起来能换，过几个月就换不了了？"举三个例子，并说出共同原因。

## A
**共同原因：** 决定本身没变，变的是**有人依赖上了它**。依赖它的人越多、越在你控制范围之外，撤回就越贵。

| 决定 | 一开始 | 后来 |
|---|---|---|
| 对外协议（REST / gRPC / GraphQL） | 换个序列化方式而已 | 每个客户都要迁移，或你永远维护旧协议的适配层 |
| 版本号规则 | 随便定一个 | 客户按它写了升级逻辑，改规则就是失信 |
| 公开声明为 stable 的 API | 改个字段名 | 任何破坏性改动都只能发新版本 endpoint |

**怎么防：**
- 对外的东西，第一天就当 one-way door 对待：写 design doc，想清楚版本策略。
- 先只给内部用户用，或者标成 beta，把"变硬"的时间往后推。
- 记下这类决定（ADR），以后的人知道它为什么撤不回。

<details class="pt" markdown="1"><summary>面试官看什么 · 配哪类故事 · 出处</summary>

**面试官在考什么：** 你是否理解"可逆性"会随时间和依赖关系变化，而不是一个静态标签。

**出处：** Orosz《The Software Engineer's Guidebook》ch25 §4「Two-way doors that become one-way doors」

</details>
