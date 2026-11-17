---
id: fluency-collections-top-k
node: fluency.collections
type: qa
step: 6
---
## Q
推荐接口对 100 万个候选打分，只要前 `limit` 名，评审说“排完序直接返回”漏了截断。取前 k 个，`sorted(...)[:k]`、`heapq.nsmallest` 各什么代价？候选不够 k 个时怎么办？

## A
**取前 k 名：堆比整体排序省，不够就少返回**

- **`sorted(items, key=…)[:k]`**：O(n log n) 时间，整个列表都排一遍；n 小或 k 接近 n 时最简单；
- **`heapq.nsmallest(k, items, key=…)`**：维护大小为 k 的堆，O(n log k) 时间，额外空间 O(k)；k 远小于 n 时更好；`nlargest` 对应取最大；
- **取前 k 的“前”由 key 决定**：排序条件是分数降序，就把降序编进 key（取负），再用 `nsmallest`；
- **并列保持确定**：key 里放 id 这类唯一字段兜底，同分的结果顺序才固定；
- **不够 k 个就少返回**：`nsmallest` 返回现有的全部，不补、不报错；
- **先过滤再截断**：先取前 k 再过滤，结果会不足 k 个；生成器表达式加 `itertools.islice` 在过滤之后截断，凑够 k 个就停（代码里的排序仍是整体排序，省下的是后面的过滤与取值）。

```python
import heapq
from itertools import islice

rows = [("m1", 4.0), ("m2", 4.5), ("m3", 4.0), ("m4", 3.0)]
order = lambda r: (-r[1], r[0])                    # 分数降序，id 升序
print(heapq.nsmallest(2, rows, key=order))         # [('m2', 4.5), ('m1', 4.0)]
print(heapq.nsmallest(10, rows, key=order)[-1])    # ('m4', 3.0)：不够 10 个，全部返回

ok = (r for r in sorted(rows, key=order) if r[1] >= 4.0)   # 先过滤
print(list(islice(ok, 2)))                                   # 再截断：凑够 2 个就停
```

**知识点：**容器的选择与惯用法（Collections Idioms）
