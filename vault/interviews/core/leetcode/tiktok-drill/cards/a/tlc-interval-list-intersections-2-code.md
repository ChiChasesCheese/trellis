---
id: tlc-interval-list-intersections-2-code
node: a.interval-list-intersections
type: qa
step: 2
---
## Q
**LC 986 区间列表的交集**｜写出 Python 实现

两个已排序、内部不相交的闭区间列表（长度各 `0..1000`，端点 `0..10^9`，`start < end`），返回它们的交集；要求线性时间。

## A
**思路。** 双指针 `i`、`j`。每轮取当前一对的 `[max(起点), min(终点)]`，非空则收下；然后让**终点较小**的那个指针前进，因为它不会再与对方后面的区间相交。

```python
def interval_intersection(first: list[list[int]], second: list[list[int]]) -> list[list[int]]:
    i = j = 0
    ans: list[list[int]] = []
    while i < len(first) and j < len(second):
        lo = max(first[i][0], second[j][0])      # 交集左端取较大的起点
        hi = min(first[i][1], second[j][1])      # 右端取较小的终点
        if lo <= hi:                             # 闭区间：lo == hi 也是一个点
            ans.append([lo, hi])
        if first[i][1] < second[j][1]:           # 终点小的那个不可能再与对方后面的区间相交
            i += 1
        else:
            j += 1
    return ans
```

运行：示例 1 → `[[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]`；`[[1,3],[5,9]]` 与 `[]` → `[]`；`[]` 与 `[[4,8],[10,12]]` → `[]`；`[[1,7]]` 与 `[[3,10]]` → `[[3,7]]`。

**复杂度。** 时间 `O(m + n)`：每轮至少一个指针前进；空间 `O(1)` 额外（结果不计）。

**写法要点。** `lo <= hi` 而不是 `<`，闭区间的单点交集必须保留；`i = j = 0` 链式赋值只用于不可变的整数；用 `else: j += 1` 把「终点相等」归到同一分支，不必单独写三路；空列表使 `while` 条件直接为假，不需要特判；结果元素用 `[lo, hi]` 列表，与输入类型一致。
