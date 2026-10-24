---
id: tlc-patterns-hashing-4-why-set-run
node: patterns.hashing
type: qa
step: 4
---
## Q
**哈希（Hashing）｜最长连续序列为什么是 `O(n)`**

LC 128 要求 `O(n)`，不排序。用集合只从「序列起点」开始数，为什么总时间仍是 `O(n)`？去掉起点判断会怎样？

## A
```python
def longest_consecutive(nums: list[int]) -> int:
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:                 # 只有 x 是某段连续序列的起点，才往后数
            y = x
            while y + 1 in s:
                y += 1
            best = max(best, y - x + 1)
    return best
```

运行：`[100,4,200,1,3,2]` → `4`；`[0,3,7,2,5,8,4,6,0,1]` → `9`；`[]` → `0`。

**为什么 `O(n)`**：每个元素最多被 `while` 数到一次——它只会被「它所在序列的起点」数到，因为只有起点才启动内层循环。所有序列互不相交，总数不超过 `n`；外层 `n` 次，内层合计 `n` 次，共 `O(n)`。

**去掉 `x - 1 not in s` 的后果**：每个元素都启动一次向后数。输入 `1..n` 时，`x=1` 数 `n` 次、`x=2` 数 `n-1` 次……共 `O(n^2)`。

- 对集合 `s` 遍历（不是对 `nums`）可以顺便去重，避免重复的值多次启动。
- 排序做法：排序后一次扫描，`O(n log n)`；面试官限制 `O(n)` 时，这是标准答案。
- 并查集也能做：`union(x, x+1)`，最大集合大小即答案，常数更大。
