---
id: craft-rule-chain-pipeline-5-across-problems-and-scales
node: craft.patterns.rule-chain-pipeline
type: qa
step: 5
---
## Q
**规则链 · 账单规则、折扣引擎、图像流水线、SQL 查询、日志处理器里的同一个骨架**｜模式

这五个问题看起来是五种东西。它们共享什么？引擎和步骤之间的分工，在哪些地方不同？

## A
**要点。** 同一个骨架：步骤实现同一个小接口，在步骤之间流动的数据类型固定，引擎只负责遍历、统一的不变量（取整、钳位、校验）、记账。新增步骤不改引擎。差别只在于每个步骤能看到什么、能不能提前停止。

```python
# billing-tax-engine：步骤看到「前面各行」
raw = rule.apply(txn, lines)

# amz-discount-engine：步骤看到「剩余价格」，引擎钳位
amount = self._bounded(discount.apply(line, remaining), remaining, discount.label)

# image-transform-pipeline：步骤只看到「上一步的图像」
for i, step in enumerate(self.steps): image = step.apply(image)

# logger：记录沿祖先链向上，每个节点的 handler 都收到；propagate=False 时停止
while node is not None:
    ...
    if not node.propagate: break
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

**见于。** billing-tax-engine、amz-discount-engine、image-transform-pipeline、amz-in-memory-db（select 的 FROM → JOIN → WHERE → ORDER BY → LIMIT → 投影）、logger。

**不变的。** 固定的数据类型、统一接口、引擎持有不变量。**变化的。** 步骤的可见范围：只看上一步的输出（图像）、看全部历史（账单行）、看剩余量（折扣）；以及能不能中断（日志的 `propagate`，折扣的「前一条把小计压到门槛以下，这一条就不再适用」）。

**信号。** 需求里出现「按顺序应用若干规则」「叠加」「再加一种规则不要改核心」「先……再……」；或者你的 `if/elif` 链每加一个需求就长一截。

**尺度对照。** 低层设计：一个循环加统一的接口。分布式：Web 框架的中间件链、Unix 管道、ETL 管线、规则引擎（Drools）。变化：步骤跑在不同机器上时，每一步的输出要持久化（否则中途失败只能从头重跑），步骤要幂等，「propagate」变成「消息路由与死信」；单进程里免费的元组传递，到分布式里就是一个队列加一次序列化。
