---
id: hft-architecture-sequencer-journal-determinism-killers
node: architecture.sequencer-journal
type: qa
step: 3
---
## Q
确定性回放要求业务逻辑是"纯函数式"的。实际代码里哪些写法会破坏确定性？时间应该怎么取？

## A
常见的破坏者：
- **读墙上时钟**（`System.nanoTime()`、`currentTimeMillis()`）：回放时是另一个时刻，结果会不同。应该用输入事件自带的（硬件）时间戳当作"当前时间"。
- **遍历 `HashMap`**：迭代顺序可能随实现或插入历史变化。
- **未固定种子的随机数**。
- **依赖线程调度**：线程从多条队列取事件的实际顺序不固定，要让日志记录"线程实际消费的顺序"，回放时按它喂。
- **依赖对象地址**（如 `identityHashCode`）。

例：策略用 `nanoTime()` 判断"行情是否已过期超过 50 µs"，回放机器更快，结论不同，回放出的订单就和线上不一样，无法复盘。
