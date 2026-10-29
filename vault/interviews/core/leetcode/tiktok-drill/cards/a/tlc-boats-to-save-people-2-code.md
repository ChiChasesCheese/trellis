---
id: tlc-boats-to-save-people-2-code
node: a.boats-to-save-people
type: qa
step: 2
---
## Q
**LC 881 救生艇**｜写出 Python 实现

数组 `people`（`1 <= people.length <= 5 * 10^4`，`1 <= people[i] <= limit <= 3 * 10^4`），每艘船最多载两人且体重之和不超过 `limit`，返回所需的最少船数。

## A
**思路。** 排序后左指针指最轻的人，右指针指最重的人。每轮：最重的人必上船；如果最轻的人也能同船（体重之和不超过 `limit`）就让他一起走。船数加一，指针向内收缩，直到两指针错开。

```python
def num_rescue_boats(people: list[int], limit: int) -> int:
    people = sorted(people)              # 排序后最轻的在左端，最重的在右端
    lo, hi = 0, len(people) - 1
    boats = 0
    while lo <= hi:                      # lo == hi 时只剩一个人，也要一艘船
        if people[lo] + people[hi] <= limit:
            lo += 1                      # 最轻的人和最重的人同船
        hi -= 1                          # 最重的人一定上船
        boats += 1
    return boats
```

运行：`[1,2], 3` → `1`，`[3,2,2,1], 3` → `3`，`[3,5,3,4], 5` → `4`，`[5], 5` → `1`，`[1,1,3,3], 4` → `2`。

**复杂度。** 时间 `O(n log n)`；空间 `O(n)`。

**写法要点。** `sorted(people)` 返回新列表，不改动输入（`people.sort()` 原地排序并返回 `None`）；循环里「最重的人一定下船」所以 `hi -= 1` 和 `boats += 1` 无条件执行，只有 `lo += 1` 是有条件的，三行各管一件事；`lo <= hi` 一个条件同时处理奇偶人数。
