---
id: tlc-incremental-memory-leak-2-code
node: b.incremental-memory-leak
type: qa
step: 2
---
## Q
**LC 1860 增长的内存泄露**｜写出 Python 实现

整数 `memory1`、`memory2`（`0 <= 它们 <= 2^31 - 1`）。从第 `1` 秒开始，每秒把 `i` 位内存分给剩余较多的内存条（相等分给第一个）；两个都不足 `i` 位时程序退出。返回 `[崩溃的秒数, 内存条 1 剩余, 内存条 2 剩余]`。

## A
**思路。** 变量 `second` 从 `1` 起；只要较大的剩余量不小于 `second`，就从较大的内存条里扣掉 `second`（平局扣第一个），`second` 加一；循环退出时的 `second` 就是崩溃时刻。

```python
def mem_leak(memory1: int, memory2: int) -> list[int]:
    second = 1                                 # 当前要分配的位数，也是秒数
    while max(memory1, memory2) >= second:     # 至少有一条放得下，程序才没崩
        if memory1 >= memory2:                 # 相等时给第一条，所以用 >=
            memory1 -= second
        else:
            memory2 -= second
        second += 1
    return [second, memory1, memory2]
```

运行：`(2, 2)` → `[3, 1, 0]`，`(8, 11)` → `[6, 0, 4]`，`(0, 0)` → `[1, 0, 0]`，`(1, 0)` → `[2, 0, 0]`，`(2^31 - 1, 2^31 - 1)` → `[92681, 88047, 41707]`。

**复杂度。** 时间 `O(sqrt(memory1 + memory2))`：每秒消耗的位数递增，`t` 秒共消耗约 `t^2 / 2`，被总量封顶；空间 `O(1)`。

**写法要点。** 把“当前秒数”和“要分配的位数”用同一个变量 `second`，少一个状态。`max(memory1, memory2) >= second` 一次表达“两个都不足才退出”的反面。平局规则落在 `>=` 上：相等时走第一个分支，不需要单独写平局。直接修改参数 `memory1`、`memory2`（`int` 不可变，函数内重新绑定不影响调用者）。返回列表，不用打包成元组。
