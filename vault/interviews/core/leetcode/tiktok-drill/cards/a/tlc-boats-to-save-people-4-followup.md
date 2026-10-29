---
id: tlc-boats-to-save-people-4-followup
node: a.boats-to-save-people
type: qa
step: 4
---
## Q
**LC 881 救生艇**｜追问

面试官接着问：（1）体重只有 `3 * 10^4` 种，能不能比 `O(n log n)` 更快？（2）每艘船可以载 `k` 个人呢？（3）要输出每艘船载了谁？

## A
1. **计数排序**：值域小，用 `Counter` 或数组数个数，再按体重从小到大展开成有序列表，后面的双指针不变。
```python
from collections import Counter


def num_rescue_boats_bucket(people: list[int], limit: int) -> int:
    cnt = Counter(people)
    ordered = [w for w in range(1, limit + 1) for _ in range(cnt[w])]
    lo, hi, boats = 0, len(ordered) - 1, 0
    while lo <= hi:
        if ordered[lo] + ordered[hi] <= limit:
            lo += 1
        hi -= 1
        boats += 1
    return boats
```
总代价 `O(n + limit)`。
2. **每船 `k` 人**：这是装箱问题，NP 难，贪心不再保证最优；常用 First-Fit Decreasing 做近似，或用状态压缩 DP 处理很小的 `n`。
3. **输出方案**：每轮把 `(people[lo], people[hi])`（能配）或 `(people[hi],)`（不能配）追加进结果列表。

**Python 提醒**：`people = people.sort()` 会把 `people` 变成 `None`；要排序并赋值，用 `sorted(people)`。
