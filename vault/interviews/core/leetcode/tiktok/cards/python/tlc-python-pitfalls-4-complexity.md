---
id: tlc-python-pitfalls-4-complexity
node: python.pitfalls
type: qa
step: 4
---
## Q
**Python 陷阱｜看起来 `O(1)` 实际是 `O(n)` 的内置操作**

哪些列表、字符串操作写在循环里会让 `O(n)` 的算法悄悄退化成 `O(n^2)`？各自的替代方案是什么？

## A
| 操作 | 实际代价 | 替代 |
|---|---|---|
| `list.pop(0)`、`list.insert(0, x)` | `O(n)` | `deque.popleft()` / `appendleft` |
| `x in list`、`list.index(x)`、`list.remove(x)` | `O(n)` | `set` / `dict`，`O(1)` |
| `a + b`（列表）、`a[i:j]` | `O(len)` 新建 | 传下标；`chain` |
| `s += c`（字符串）循环累加 | 最坏 `O(n^2)` | 收集成 `list`，最后 `"".join` |
| `del a[0]`、`a[:k]` 头部删除 | `O(n)` | 双指针 / 下标 |
| `s.count`、`s.find`、`s in t` | `O(n)` 到 `O(nm)` | 预处理 / KMP / 哈希 |
| `len(x)`、`x[i]`、`append`、`pop()` | `O(1)` | 无需替代 |

```python
from collections import deque
q = deque(range(50000))
while q:
    q.popleft()           # 全部 O(1)；换成 list.pop(0) 在 5 万个元素上已经慢 20 倍以上
```

- `x in list` 在循环里是最常见的：LC 1、3、128 如果用列表判断「出现过没有」，会超时；一律先把查询集合变成 `set`。
- `sorted` / `min` / `max` 本身 `O(n)` 或 `O(n log n)`，放在 `for` 里每次重算，也会多一个 `n` 因子；能增量维护的（堆、单调队列）就别每次重算。
- 面试时说出每一行的复杂度：「`pop(0)` 是 `O(n)`，所以我用 `deque`」比只写出代码更有说服力。
- **坑**：`list.remove(x)` 只删**第一个**匹配；遍历列表时删元素会跳过后一个元素（`[1,2,3,4]` 边遍历边删偶数，得到 `[1, 3]` 碰巧正确，换成连续偶数就漏删），要遍历副本或用推导式重建。
