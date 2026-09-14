---
id: cc-verification-invariant-conservation
node: verification.invariants
type: qa
---
## Q
Name three conservation invariants you can assert in almost any assessment problem, and the bug each one catches.

## A
**Conservation compares a whole against the sum of its parts.**

- **Money splits sum back to the total exactly.** Catches a rounding rule applied per row instead of once at the edge — the classic one-cent-short bug.
- **`sum(len(members[t]) for t in targets) == len(active)`.** Catches an entity removed from one index and left in the other ([[cc-verification-invariant-two-indexes]]).
- **Apply an event, then un-apply it, and the state equals what it was.** Catches a decrement that forgets one of the counters the increment touched — the single most common reversal bug.

Each is one line, lives in a test, and fails loudly on exactly the class of bug hidden tests are built from.

## Q zh
说出三条几乎在任何笔试题里都能断言的守恒不变量，以及各自抓到的 bug。

## A zh
**守恒就是拿整体和它各部分之和做比较。**

- **金额拆分之和精确等于总额。** 抓的是逐行舍入而非在边缘只舍入一次 —— 经典的「差一分」bug。
- **`sum(len(members[t]) for t in targets) == len(active)`。** 抓的是实体从一个索引里移除、却留在另一个索引里（[[cc-verification-invariant-two-indexes]]）。
- **施加一个事件再撤销它，状态与原来相等。** 抓的是「递减时漏掉了递增碰过的某个计数器」—— 最常见的冲正 bug。

每条都是一行，住在测试里，并且恰好在隐藏测试所构建的那类 bug 上大声失败。
