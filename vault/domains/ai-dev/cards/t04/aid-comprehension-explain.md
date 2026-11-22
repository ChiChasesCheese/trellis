---
id: aid-comprehension-explain
node: t04.comprehension-debt
type: qa
step: 2
tags: [考点]
---
## Q
**Comprehension debt · 解释检验**｜考点 · 必会

agent 重写了重试逻辑，测试全绿，diff 200 行。你的同事问："为什么重试要用指数退避加抖动，而不是固定间隔？"你答不上来。该合并吗？

## A
**不该。** 答不上"为什么"，说明你没读懂这块；合并后它是你的责任。

| 选项 | 做法 |
|---|---|
| 理解它 | 让 agent 解释这个选择、要解决的失败场景，**你复述**；对照文档核实说法 |
| 简化它 | 让 agent 重写成你能解释的更简单版本，如固定间隔加最大次数 |
| 记下原因 | 理解后把"为什么"写进注释或提交说明，下个人不再重复这个问题 |

**判断标准：** 不是"agent 的解释听起来对"，而是"我能不看稿向同事说清楚"。

**别做：** 因为"测试过了""AI 写的应该有道理"就合并。

<details class="pt" markdown="1"><summary>出处</summary>

Claude Code docs《Security》（User responsibility：你有责任在批准前审查提议的代码和命令）

</details>
