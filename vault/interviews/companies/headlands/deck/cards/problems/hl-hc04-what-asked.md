---
id: hl-hc04-what-asked
node: problems.hc04-queue-mean-snapshot
type: qa
step: 1
---
## Q
队列均值与快照（Queue Mean + Snapshot）题问什么？四个 Part 各加了什么要求？

## A
实现一个 FIFO 队列（元素是 `long`）和 `push`、`pop`、`get_mean`（所有元素的平均数）。例：push 1、2、3 → 均值 2.0；push 4 → 2.5；pop 返回 1 → 均值 3.0。

- **Part 1**：每个操作均摊 **O(1)**；均值**精确**（不能用 `double` 维护总和）；**不溢出**（元素可以是 `Long.MAX_VALUE`）；`getMean()` 返回最接近精确值的 `double`；空队列 `pop/getMean` 抛 `NoSuchElementException`；另提供约分分数 `Mean`。
- **Part 2**：事件流 `Push / Pop / Query / Correct`，`Correct`（修正快照）丢掉此前整段逻辑历史，队列内容变成快照给的列表；文本格式 `push N`、`pop`、`mean`、`snapshot [N ...]`，错误带行号。
- **Part 3**：版本化 / 持久化队列，保留每个历史版本，查任意版本均值，能从旧版本分叉，不能每个版本复制一份。
- **Part 4**：单写者、多读者，读者不加锁、不阻塞写者、永远读到一致值。

面试官真正在看：你是否**主动**说出浮点累积误差、`long` 溢出、空队列行为、快照是拷贝还是共享、多线程读。「O(1) 均值」只是门槛。
