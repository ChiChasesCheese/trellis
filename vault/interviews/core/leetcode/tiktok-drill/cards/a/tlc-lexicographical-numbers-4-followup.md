---
id: tlc-lexicographical-numbers-4-followup
node: a.lexicographical-numbers
type: qa
step: 4
---
## Q
**LC 386 字典序排数**｜追问

面试官接着问：（1）要求惰性输出、内存真正 `O(1)`？（2）只要字典序第 `k` 小的数，能不能不逐个走？（3）用 Python 内置排序行不行？

## A
1. **惰性输出**：把 `result.append(cur)` 换成 `yield cur`，调用方边取边用。
```python
from collections.abc import Iterator


def lexical_iter(n: int) -> Iterator[int]:
    cur = 1
    for _ in range(n):
        yield cur
        if cur * 10 <= n:
            cur *= 10
        else:
            while cur % 10 == 9 or cur + 1 > n:
                cur //= 10
            cur += 1
```
2. **第 `k` 小**（LC 440）：在十叉树上先算「以 `x` 为根的子树里有多少个不超过 `n` 的数」，`k` 比它大就跳到右兄弟，否则下沉；每步 `O(log n)`，整体 `O(log^2 n)`。
3. **内置排序**：`sorted(range(1, n + 1), key=str)` 一行就能通过正确性，但是 `O(n log n)`，且要为每个数造字符串，不满足题目要求，面试里只作为暴力基线。

**Python 提醒**：`Iterator` 来自 `collections.abc`（`from collections.abc import Iterator`）；`sorted(map(str, …))` 会得到字符串列表，别忘了转回整数。
