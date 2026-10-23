---
id: hl-mm01-mutations
node: problems.mm01-fizzbuzz
type: qa
step: 4
---
## Q
FizzBuzz 的测试用 7 个错误版本验证，分别是哪些、各会错在哪里？变异检查（mutation check）是什么？

## A
| 错误版本 | 挂几个测试 | 错在哪里 |
|---|---|---|
| 先判断 3，再判断 15 | 5 | 15、30、45 打印成 `Fizz` |
| `i < n` | 12 | 少打最后一行 |
| 从 `i = 0` 开始 | 12 | 多打一行 `FizzBuzz`（0 能被 15 整除） |
| `"Fizzbuzz"` 大小写不对 | 5 | 输出要逐字一致 |
| 用空格代替换行 | 12 | 题目要求一行一个 |
| 每行末尾多一个空格 | 12 | 比对是逐字的 |
| 自己的 `PrintWriter` 没有 `flush()` | 12 | 什么都没输出 |

**变异检查**：先确认参考解全绿（12/12），再要求每个故意写错的版本都真的让某个测试失败；「没有测试被选中」（比如 `-Dtest` 写错了）不算抓到。**测试全绿不能证明什么，要用故意写错的版本验证测试本身。**

运行方式：`mvn -q test -Dimpl=starter -Dtest='headland/q01/**'` 跑你的 Starter；去掉 `-Dimpl` 跑参考解；`python3 mutation_check.py q01`。

循环上界要 `<= n`（`i < n` 少打最后一行），起点是 1（从 0 开始会多打一行）。
