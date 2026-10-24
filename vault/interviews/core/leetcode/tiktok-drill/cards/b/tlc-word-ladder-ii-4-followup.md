---
id: tlc-word-ladder-ii-4-followup
node: b.word-ladder-ii
type: qa
step: 4
---
## Q
**LC 126 单词接龙 II**｜追问

面试官接着问：（1）只要最短路径的条数，不要列出来；（2）字典有 `10^5` 个词，BFS 还能怎么加速；（3）只要任意一条最短路径，怎么改。

## A
1. **只要条数**：最短路条数是父亲表上的计数 DP，不需要展开路径，可以在极大输出规模下仍然高效。

```python
from functools import cache


def count_paths(parents: dict[str, list[str]], begin: str, end: str) -> int:
    @cache
    def go(w: str) -> int:
        return 1 if w == begin else sum(go(p) for p in parents[w])
    return go(end)
```

示例 1 的父亲表 → `2`；字典是 `a`、`b`、`c`、`d` 组成的全部 `4` 位单词，从 `aaaa` 到 `dddd` → `24` 条（等于展开后的路径数）。递归深度是最短路长度。
2. **加速**：双向 BFS，从起点和终点各维护一层，每次扩展较小的一侧，在两侧第一次相遇的层停止；分支因子大时访问的节点数从 `b^d` 降到约 `2 * b^(d/2)`。通配符桶让每次找邻居是 `O(L)` 次查表，而不是枚举 `26 * L` 个替换再查字典。
3. **任意一条**：`parents[w]` 只保留第一个父亲，`dfs` 变成一路向前的循环；若只要最短长度（LC 127），连父亲都不用记，BFS 的层数就是答案。

**Python 提醒**：`functools.cache` 要求参数可哈希，这里的单词是字符串，满足；`parents` 本身不可哈希，所以放在闭包里而不是作为缓存参数。回溯里要保存结果必须拷贝路径（`path[::-1]` 或 `list(path)`），否则所有结果都指向同一个被不断修改的列表。
