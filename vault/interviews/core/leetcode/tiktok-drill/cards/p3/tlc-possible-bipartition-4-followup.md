---
id: tlc-possible-bipartition-4-followup
node: p3.possible-bipartition
type: qa
step: 4
---
## Q
**LC 886 可能的二分法**｜追问

面试官接着问：（1）不用 BFS，用并查集（Union-Find）能做吗？（2）边是一条一条在线到来的，每来一条要立刻回答「现在还能二分吗」？（3）分成 `k` 组（`k >= 3`）呢？

## A
1. **并查集的「敌人」技巧**：对每个人记一个「某个敌人」`enemy[u]`。读到一对 `(a, b)`：若 `a` 已有敌人 `x`，则 `x` 必须和 `b` 同组，合并 `x` 与 `b`；`b` 同理。最后若 `a` 与 `b` 落在同一集合，说明冲突。
```python
def possible_bipartition_dsu(n: int, dislikes: list[list[int]]) -> bool:
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    enemy = [0] * (n + 1)                          # enemy[u]：u 的某个敌人（0 = 还没有）
    for a, b in dislikes:
        for u, v in ((a, b), (b, a)):
            if enemy[u] == 0:
                enemy[u] = v
            else:
                parent[find(enemy[u])] = find(v)   # u 的所有敌人必须同组
        if find(a) == find(b):
            return False
    return True
```
2. **在线加边**：并查集天然支持，每加一条边做上面的合并并检查，均摊接近 `O(1)`；BFS 染色则要在新边连接了两个已染色的块时重新对齐颜色，不方便。另一种做法是「带奇偶的并查集」：每个点记录到根的奇偶，合并时校正。
3. **`k >= 3` 组**：这是图的 `k` 着色问题，`k >= 3` 时是 NP 完全的，没有多项式算法，只能回溯加剪枝或启发式（如 DSATUR）。`k = 2` 之所以简单，是因为选择被完全强制。

**Python 提醒**：用 `color = [0] * (n + 1)` 建一维数组没有别名问题；但邻接表要写 `[[] for _ in range(n + 1)]`，写成 `[[]] * (n + 1)` 会让所有点共用同一个列表，每条边被加到所有点上，结果全部错乱。`dislikes` 的元素是长度为 2 的列表，`for a, b in dislikes` 可直接解包。
