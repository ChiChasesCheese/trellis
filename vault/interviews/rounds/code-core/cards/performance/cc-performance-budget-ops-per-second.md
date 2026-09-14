---
id: cc-performance-budget-ops-per-second
node: performance.budget
type: qa
---
## Q
You must decide in 60 seconds, with no profiler, whether a plan is fast enough. What single number do you carry, and how do you apply it to "10^6 rows, each doing a dict lookup and a string format"?

## A
**~10^7 simple bytecode operations per second** for pure Python; 10^8–10^9 for work that happens inside C (`str.split`, `sorted`, `sum`, `bytes` slicing).

10^6 rows × ~10 interpreted operations ≈ 10^7 → about one second. That fits a 2-second budget with no room to spare, so keep per-row work down: no regex compiled per row, no `Decimal` per row, no formatting a string you will not print.

The estimate only has to be right to a factor of ten — that is enough to separate "fine" from "quadratic", which is the only question you are answering.

## Q zh
没有 profiler，你必须在 60 秒内判断一个方案够不够快。你随身带的那个数字是什么？怎么把它用在「10^6 行，每行一次 dict 查找加一次字符串格式化」上？

## A zh
**纯 Python 每秒约 10^7 次简单字节码操作**；跑在 C 里的工作（`str.split`、`sorted`、`sum`、`bytes` 切片）是 10^8–10^9。

10^6 行 × 每行约 10 次解释器操作 ≈ 10^7 —— 大约一秒。这塞进 2 秒预算已经没有余量，所以要压低每行的工作量：不要每行编译一次正则，不要每行造一个 `Decimal`，不要格式化一个不会打印的字符串。

这个估算只要在十倍量级上正确就够了 —— 那足以分开「没问题」和「平方复杂度」，而这正是你唯一要回答的问题。
