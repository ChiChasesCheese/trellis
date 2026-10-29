---
id: tlc-count-the-hidden-sequences-4-followup
node: a.count-the-hidden-sequences
type: qa
step: 4
---
## Q
**LC 2145 统计隐藏数组数目**｜追问

面试官接着问：（1）数据是流式的，不能存下整个 `differences`？（2）要把所有合法的隐藏数组列出来？（3）如果还要求隐藏数组里的元素互不相同？

## A
1. **流式**：只需要当前前缀和以及目前见过的最大、最小前缀和，三个变量，`O(1)` 空间：

```python
def number_of_arrays_stream(differences: list[int], lower: int, upper: int) -> int:
    cur = hi = lo = 0                          # 当前前缀和、见过的最大 / 最小前缀和（含起点的 0）
    for d in differences:
        cur += d
        hi, lo = max(hi, cur), min(lo, cur)
    return max(0, (upper - lower) - (hi - lo) + 1)
```

2. **列出所有数组**：起点 `x` 从 `lower - min(prefix)` 取到 `upper - max(prefix)`，每个起点生成 `[x + p for p in prefix]`；个数乘 `n + 1` 就是输出规模，所以只有个数很小时才能列出。
3. **元素互不相同**：此时必须逐个检查，因为“互不相同”只取决于 `prefix` 里有没有重复值：若 `prefix` 有重复，答案是 `0`；否则合法起点个数不变。可以用 `len(set(prefix)) == len(prefix)` 判断，`O(n)`。

**Python 提醒**：`itertools.accumulate` 返回迭代器，只能遍历一次；需要多次用时先转成列表（`[0, *accumulate(...)]` 已经是列表）。`hi, lo = max(hi, cur), min(lo, cur)` 是同时更新，右边先整体求值。
