---
id: cc-output-sentinels-empty-input
node: output.sentinels
type: qa
---
## Q
The input is a header line and nothing else. What must each part print?

## A
**Run every part against empty input before submitting; the answer is usually not "nothing".**

- A part that aggregates prints its labels with zeroes: `SKIPPED: 0`, `MAX_RESERVE: 0.00`.
- A part that lists prints its sentinel ([[cc-output-sentinels-none-vs-blank]]).
- A part that echoes rows prints nothing at all.

The crashes to pre-empt:
- `max()` / `min()` over an empty sequence raises — pass `default=`.
- A division by a count that can be zero: decide what 0/0 means (usually 0, sometimes "excluded from the average" — an all-zero group is a graded case).
- `lines[0]` on an empty input, and a `split()` that returns fewer fields than you unpack.

It costs thirty seconds to test and it is in essentially every hidden suite.

## Q zh
输入只有一行 header，别的什么都没有。每个 part 该打印什么？

## A zh
**提交前用空输入跑一遍每个 part；答案通常不是「什么都不打印」。**

- 做聚合的 part 打印带零值的标签：`SKIPPED: 0`、`MAX_RESERVE: 0.00`。
- 做列表的 part 打印它的哨兵（[[cc-output-sentinels-none-vs-blank]]）。
- 只回显行的 part 什么都不打印。

需要预先挡住的崩溃：
- 对空序列调用 `max()` / `min()` 会抛异常 —— 传 `default=`。
- 除以一个可能为零的计数：决定 0/0 是什么（通常是 0，有时是「不计入平均」—— 全零分组是会被判分的情形）。
- 空输入上的 `lines[0]`，以及返回字段数少于你解包个数的 `split()`。

这个测试花三十秒，而且几乎每套隐藏用例里都有。
