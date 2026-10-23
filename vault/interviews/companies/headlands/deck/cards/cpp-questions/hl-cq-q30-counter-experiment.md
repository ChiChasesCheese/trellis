---
id: hl-cq-q30-counter-experiment
node: cpp-questions.g-concurrency
type: qa
step: 14
---
## Q
4 个线程各对计数器加 50 万次（期望共 200 万），用 `volatile int`（`v = v + 1`）、`atomic<int>::fetch_add`、`mutex` + 普通 `int` 三种方式，结果各是多少？

## A
- `volatile int`：**1995942**，丢了更新（lost updates），而且每次运行数字都不同——这就是竞争。
- `atomic<int>`：2000000。
- `mutex + int`：2000000。
- 修法：`std::atomic`（单个变量）、`std::mutex`（一段逻辑），或让每个线程用自己的局部计数最后相加（无共享）。
