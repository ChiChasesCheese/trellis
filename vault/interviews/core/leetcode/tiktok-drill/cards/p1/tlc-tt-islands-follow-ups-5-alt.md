---
id: tlc-tt-islands-follow-ups-5-alt
node: p1.tt-islands-follow-ups
type: qa
step: 5
---
## Q
**岛屿数量及其追问集合**｜另一种解法

不用 DFS，数 `0/1` 网格里的岛屿（四方向相连）并且支持「一行一行流式读入、只保存上一行」，该怎么做？

## A
**并查集逐行扫描。** 每个新陆地格只看上方、左方：都是水就新建一座岛（计数加 1）；否则取它们的根，不同则合并（计数减 1）。每行结束后只保留仍出现在这一行的根，内存 `O(n)`。

```python
from collections.abc import Iterable, Sequence


def count_islands_stream(rows: Iterable[Sequence[int]]) -> int:
    """逐行读入，只保存上一行的标签；内存 O(n)，n 为列数。"""
    parent: dict[int, int] = {}
    prev: list[int] = []                        # 上一行每格的标签，-1 表示水
    count = next_label = 0

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for row in rows:
        cur = [-1] * len(row)
        for c, v in enumerate(row):
            if not v:
                continue
            near = [lab for lab in (prev[c] if prev else -1, cur[c - 1] if c else -1) if lab >= 0]
            if not near:                        # 上、左都是水：新岛
                parent[next_label] = cur[c] = next_label
                next_label += 1
                count += 1
                continue
            root = find(near[0])
            cur[c] = root
            for lab in near[1:]:
                other = find(lab)
                if other != root:               # 上、左属于不同的岛：合并，总数减一
                    parent[other] = root
                    count -= 1
        prev = [find(lab) if lab >= 0 else -1 for lab in cur]
        parent = {lab: lab for lab in set(prev) if lab >= 0}    # 只保留仍在边界行上的标签
    return count
```

`[[1,1,0,0,0],[1,1,0,0,0],[0,0,1,0,0],[0,0,0,1,1]]` → `3`，`[[1,0,1],[1,1,1]]` → `1`（第二行把两座岛合并）。时间 `O(mn α)`，空间 `O(n)`。

**怎么选。** 网格能整个放进内存：递归 DFS 最短最不易错（太深时换显式栈）。网格是流或超大：用这版（分块处理同理，块边界上再合并）。只要最大面积等统计：DFS 更直接。
