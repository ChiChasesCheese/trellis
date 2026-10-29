---
id: tlc-minimum-number-of-arrows-to-burst-balloons-4-followup
node: b.minimum-number-of-arrows-to-burst-balloons
type: qa
step: 4
---
## Q
**LC 452 用最少数量的箭引爆气球**｜追问

面试官接着问：（1）要返回每支箭的具体位置？（2）改成「最少删除多少个区间，使剩下的互不重叠」（LC 435）？（3）气球改成开区间怎么办？

## A
1. **射点位置**：每次新射一支就记录 `end`：

```python
from operator import itemgetter


def arrow_positions(points: list[list[int]]) -> list[int]:
    shots: list[int] = []
    for start, end in sorted(points, key=itemgetter(1)):
        if not shots or start > shots[-1]:
            shots.append(end)
    return shots
```
   运行：`[[10,16],[2,8],[1,6],[7,12]]` → `[6, 12]`，`[[1,2],[3,4],[5,6],[7,8]]` → `[2, 4, 6, 8]`，`[[1,2],[2,3],[3,4],[4,5]]` → `[2, 4]`。
2. **LC 435**：最少删除数 = `n` 减去最多能保留的两两不相交区间数。保留数用同一个右端点排序扫描得到，只是相接的区间**不算重叠**，条件写成 `start >= last`（相接可以保留）。`[[1,2],[2,3],[3,4],[1,3]]` → `1`，`[[1,2],[1,2],[1,2]]` → `2`，`[[1,2],[2,3]]` → `0`。两题是同一个扫描，区别只在等号：射箭里端点相接算相交（`>`），LC 435 里相接不算重叠（`>=`）。
3. **开区间**：端点相接的两个气球不能被同一个位置射中，条件改为 `start >= last`，其余不变。

**Python 提醒**：`sorted(points, key=itemgetter(1))` 不会改变调用者的 `points`；`points.sort(...)` 会原地修改，面试里如果输入不允许被改，要用前者。排序是稳定的，右端点相同的气球保持原有相对顺序，不影响结果。
