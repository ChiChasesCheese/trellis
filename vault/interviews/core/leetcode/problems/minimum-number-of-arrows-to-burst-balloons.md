---
slug: minimum-number-of-arrows-to-burst-balloons
---
## Q
**LC 452 用最少数量的箭引爆气球**｜Medium

气球是 `x` 轴上的闭区间，一支竖直的箭能射爆所有包含该 `x` 的气球，求引爆全部气球的最少箭数。

## A
**一句话。** 区间贪心：按右端点排序，新气球够不着上一支箭就新射一支，射在它的右端点。

```python
def find_min_arrow_shots(points):
    arrows = 0
    last = -inf                    # 上一支箭的位置
    for start, end in sorted(points, key=itemgetter(1)):
        if start > last:           # 够不着：新射一支
            arrows += 1
            last = end
    return arrows
```

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**易错点。**
- 条件写成 `start >= last`：端点相接可共用一支箭，`[[1,2],[2,3],[3,4],[4,5]]` 得 `4`，应为 `2`。
- 按左端点排序却不收缩右边界：`[[1,10],[2,3],[4,5]]` 一直用 `10` 当边界，得 `1`，应为 `2`。
- 排序用 `a[1] - b[1]`：定宽整数语言里会溢出（坐标到 `±2^31`）。

**追问。**
- 气球改成开区间？：端点相接不能共用，条件改为 `start >= last`。
- 要返回射点？：每次新射时记录 `end`。

**同模式。** LC 435 无重叠区间、LC 56 合并区间、LC 646 最长数对链、LC 1288 删除被覆盖区间
