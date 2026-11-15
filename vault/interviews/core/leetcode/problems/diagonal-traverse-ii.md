---
slug: diagonal-traverse-ii
---
## Q
**LC 1424 对角线遍历 II**｜Medium

`nums` 是长短不一的二维列表（总数 `<= 10^5`）。按反对角线顺序输出：`i + j` 小的先输出，同一条反对角线上从下往上（行号大的先）。

## A
**一句话。** 同一条反对角线 `i + j` 相同；按行顺序扫描把元素放进 `i + j` 的桶，桶内是行号递增，输出时反转即可。只扫存在的元素，不补成矩形。

```python
def find_diagonal_order(nums):
    groups = defaultdict(list)   # i + j -> 元素，按 i 递增
    for i, row in enumerate(nums):
        for j, x in enumerate(row):
            groups[i + j].append(x)
    ans = []
    for s in sorted(groups):
        ans.extend(reversed(groups[s]))  # 同组从下往上
    return ans
```

**复杂度。** 时间 `O(N)`（`N` 为元素总数，桶号连续可不排序），空间 `O(N)`。

**易错点。**
- 补成 `max行 × max列` 的矩形再遍历：行很长时达到 `10^10` 个格子。
- 忘了反转：桶里是从上往下，题目要从下往上。

**追问。**
- BFS 写法？：从 `(0, 0)` 出发，每个格子先放下方 `(i+1, 0)`（只在 `j = 0` 时）再放右边 `(i, j+1)`，出队顺序就是答案。
- 和 LC 498 有什么不同？：那题是完整矩形、方向交替；这题行长不一、方向固定。

**同模式。** LC 54 螺旋矩阵、LC 498 对角线遍历、LC 1329 将矩阵按对角线排序
