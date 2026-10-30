---
id: tlc-longest-consecutive-sequence-2-code
node: p3.longest-consecutive-sequence
type: qa
step: 2
---
## Q
**LC 128 最长连续序列**｜写出 Python 实现

整数数组 `nums`（长度 `0..10^5`，值 `-10^9..10^9`，可有重复）。返回其中数值上连续的最长序列的长度（如 `3,4,5`；元素在原数组中的位置无关）。要求 `O(n)`，不能靠排序。

## A
**思路。** 先把数放进集合（顺便去重）。遍历集合里的每个 `x`：如果 `x - 1` 也在集合里，说明 `x` 不是序列起点，直接跳过；否则 `x` 是起点，向右一格格检查 `x+1, x+2, …` 是否在集合里，数出序列长度，更新答案。

```python
def longest_consecutive(nums: list[int]) -> int:
    seen = set(nums)                   # 去重 + O(1) 查询
    best = 0
    for x in seen:
        if x - 1 in seen:              # x 不是序列的起点：跳过，让起点去数
            continue
        end = x + 1
        while end in seen:             # 从起点向右数下去
            end += 1
        best = max(best, end - x)
    return best
```

运行：`nums=[100,4,200,1,3,2]` → `4`，`nums=[0,3,7,2,5,8,4,6,0,1]` → `9`，`nums=[1,0,1,2]` → `3`，`nums=[]` → `0`，`nums=[-10**9, 10**9]` → `1`，`nums=list(range(10**5))` → `100000`。

**复杂度。** 时间 `O(n)`：每个数最多被「数一次」覆盖——只有序列起点才会往右数，而每个非起点的数恰好被它所在序列的起点数到一次；空间 `O(n)`（集合）。

**写法要点。** `set(nums)` 一步去重并获得 `O(1)` 的 `in`；`if x - 1 in seen: continue` 用提前 `continue` 保持主逻辑少一层缩进；`end` 记录序列的右端（开区间），长度就是 `end - x`；遍历 `seen` 而不是 `nums`，防止重复元素重复计算。空数组时 `best = 0` 即返回 `0`，不需要特判。
