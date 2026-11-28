---
id: mlp-coding-pc12-followups
node: coding.pc12
step: 2
type: qa
---
## Q
**盈亏计算（PnL）：追问与变体**｜编程轮

PnL 写完后，面试官会往哪些方向追问？

## A
- **FIFO 以外的配对方式：** 加权平均成本法（average cost）只用一个数字：持仓数量和平均成本，买入时更新平均价，卖出时按平均价算盈亏，不需要队列，更简单；后进先出（LIFO）把队列换成栈。会计和税务口径不同，面试时先问清用哪种。
- **总盈亏怎么核对：** 总盈亏等于已实现加未实现再扣手续费；把所有成交的现金流（卖得为正、买入为负）加上持仓按最新价的市值，应当得到同一个数，用它当测试的对账断言。
- **手续费的两种口径：** 按笔固定收取，或按成交金额的比例收取；比例手续费要在循环里用 `qty * px * rate` 算，不能写成固定值。手续费算进已实现盈亏，而不是未实现。
- **缺最新价：** `marks[s]` 找不到就是 `KeyError`；按需求选择是报错，还是只算已实现盈亏、把这个 symbol 的未实现标为缺失，不要悄悄当 0。
- **多币种：** 每个 symbol 的盈亏先用当时的汇率换成基础货币，再相加，和价格存储里换算汇率是同一个做法。
- **卖出数量超过持仓：** 本题的答案是允许，超出的部分开空头；如果需求是禁止卖空，在开新批次之前检查并抛 `ValueError`。
- **会多花一个测试用例的边界：** 完全平仓后再开反方向的仓；一笔成交跨多个批次；同 symbol 多笔交织；全部平仓后未实现为 0；数量为 0 的成交；价格用 `float` 的精度问题。

**英文答法。**
- "FIFO is one convention; **average cost** is simpler, just a running quantity and average price. I'd ask which one they want."
- "As a check, **realized plus unrealized equals cash flow plus mark-to-market value**."
- "If a symbol has no mark price, I'd **raise** rather than silently treat it as zero."
