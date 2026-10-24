---
id: tlc-python-pitfalls-7-input-scale
node: python.pitfalls
type: qa
step: 7
---
## Q
**Python 陷阱｜算法对了却超时：Python 常数怎么压**

`n = 10^5` 的题，`O(n log n)` 的 Python 代码仍超时，常见原因是什么？有哪些低成本的优化？

## A
Python 约每秒执行 `10^7` 条简单语句，C++ 约 `10^8` 到 `10^9`。同样的 `O(n log n)`，Python 的常数大 30 倍以上，所以数据范围上限要保守估计。

| 现象 | 原因 | 处理 |
|---|---|---|
| 循环里调用内置 `sorted`、`min`、`sum` 很快，手写同样逻辑很慢 | 内置函数在 C 层 | 能用内置就用内置，如 `sum(map(...))`、`sorted` |
| 外层循环里反复属性访问 `self.x`、`heapq.heappush` | 每次查找都花时间 | 局部别名：`push = heapq.heappush` |
| 递归 + 记忆化状态上百万 | 函数调用开销大 | 自底向上的循环 DP |
| `list` 当队列、`in list` | 隐藏的 `O(n)` | `deque`、`set` |
| 二维 DP 每格新建对象 | 内存分配 | 预先开好 `[0] * (n + 1)`，滚动数组 |
| 大量小对象（节点类） | 每个实例带 `__dict__` | `__slots__`；或用数组下标代替对象 |

- 先估算：`n * log n` 约 `1.7 * 10^6` 次基本操作（`n = 10^5`），Python 可接受；`n * m = 10^8` 的二维 DP 在 Python 里不行，要换算法或用 `numpy`。
- 输入输出大时（本地读测试数据）：`sys.stdin.readline` 比 `input()` 快；LeetCode 上函数签名固定，不用操心。
- 面试写完后说一句「`n` 上限 `10^5`，所以我用 `O(n log n)`」，比盲目追求 `O(n)` 更重要。
- **坑**：优化常数前先确认复杂度：把 `O(n^2)` 的写法调快 5 倍仍然是 `O(n^2)`。
