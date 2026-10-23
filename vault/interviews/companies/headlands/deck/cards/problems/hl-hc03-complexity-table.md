---
id: hl-hc03-complexity-table
node: problems.hc03-recursive-sum
type: qa
step: 17
---
## Q
递归、迭代、trampoline、闭式、并行求和的时间与栈 / 额外空间复杂度分别是什么？

## A
- **递归**：时间 O(n)，栈 O(n)。
- **迭代**：时间 O(n)（n = 3×10⁸ 约 77 ms），空间 O(1)。
- **trampoline**：时间 O(n)（n = 5×10⁶ 约 14 ms），堆上活跃对象 O(1)，GC 压力 O(n)。
- **`rangeSum` 闭式**：O(1) 时间，O(1) 空间（快路径无分配）。
- **并行求和**：O(N / p + log p)，任务 O(p)。

这里 n 是输入整数本身，不是输入「长度」。迭代对 `Long.MAX_VALUE` 附近的 n 要 40 亿步，只能走闭式。

速记：`O(n)` 线性增长；`O(log n)` n 翻倍只多一步；`O(n²)` 每对元素都处理；`O(1)` 与 n 无关。

阈值数字：`int` 在 n=65536 溢出；`long` 在 n=4 294 967 296 溢出；默认 1 MiB 栈 `sumToRecursive(65536)` 就爆栈（40000 还行）。

测试边界清单：`n = 0 / 1 / < 0`；`Long.MAX_VALUE` 附近；`INT` 位宽 65535 / 65536，`LONG` 位宽 4294967295 / 4294967296；区间：单点、`a==b==0`、全负、跨 0、`MIN..MAX`、`MAX-1..MAX`、`MIN..0`、`a>b`；数组：空、单元素、块数 > 元素数、`threshold=1`、块内溢出但总和不溢出；栈：512 KiB / 64 MiB 线程栈，100 万层 `More` 链，200 万层互递归。
