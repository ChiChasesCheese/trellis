---
id: tlc-number-of-provinces-4-followup
node: p4.number-of-provinces
type: qa
step: 4
---
## Q
**LC 547 省份数量**｜追问

省份数量已经用递归 DFS 做到 `O(n^2)`。面试官接着问：（1）`n` 很大，递归会爆栈怎么办？（2）输入改成边列表，或者边一条条在线到来，每来一条边要报告当前省份数？（3）要列出每个省份里有哪些城市？

## A
1. **不递归**：显式栈，入栈时就标记，每个城市只入栈一次，`O(n^2)` 时间。递归版的深度最坏是一条链，等于 `n`，CPython 默认递归上限约 `1000`。

```python
def find_circle_num_stack(is_connected: list[list[int]]) -> int:
    n = len(is_connected)
    seen = [False] * n
    provinces = 0
    for start in range(n):
        if seen[start]:
            continue
        provinces += 1
        seen[start] = True                        # 入栈时就标记，每个城市只入栈一次
        stack = [start]
        while stack:
            i = stack.pop()
            for j in range(n):
                if is_connected[i][j] and not seen[j]:
                    seen[j] = True
                    stack.append(j)
    return provinces
```

2. **边列表或在线加边**：并查集（union-find）。初始 `n` 个省份，每条边两端的根不同就合并并让计数减一，每条边近似 `O(α(n))`，随时可读当前计数。

```python
class Provinces:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.count = n                            # 当前省份数

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]   # 路径折半
            x = self.parent[x]
        return x

    def connect(self, a: int, b: int) -> int:     # 加一条边，返回当前省份数
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb
            self.count -= 1
        return self.count
```

3. **列出每个省份**：并查集结束后用 `defaultdict(list)` 按 `find(i)` 分组；或在 DFS 里把访问到的城市追加进列表，一次 DFS 一个列表。

**Python 提醒**：`seen = [False] * n` 没问题（元素是不可变的 `bool`），但二维标记数组不能写 `[[False] * n] * n`，那是 `n` 个指向同一行的引用；要写 `[[False] * n for _ in range(n)]`。
