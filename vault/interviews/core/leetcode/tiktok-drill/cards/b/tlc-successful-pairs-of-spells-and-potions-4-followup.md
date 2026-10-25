---
id: tlc-successful-pairs-of-spells-and-potions-4-followup
node: b.successful-pairs-of-spells-and-potions
type: qa
step: 4
---
## Q
**LC 2300 咒语和药水的成功对数**｜追问

面试官接着问：（1）不用二分，能不能线性扫描？（2）药水的值域只有 `10^5`，能不能 `O(1)` 回答一个咒语？（3）药水会动态增加？分别怎么改。

## A
1. **双指针**：把咒语的下标按咒语**从小到大**排序，药水升序，成功药水从最大的一端数起，用 `j` 表示已确认成功的个数。咒语越大，需要的药水门槛越低，成功的药水只增不减，`j` 不回退：

```python
def successful_pairs_two_pointers(spells: list[int], potions: list[int], success: int) -> list[int]:
    potions = sorted(potions)
    m = len(potions)
    ans = [0] * len(spells)
    j = 0                                           # 已确认成功的药水个数（从最大的一端数起）
    for i in sorted(range(len(spells)), key=lambda i: spells[i]):   # 咒语从小到大
        while j < m and potions[m - 1 - j] * spells[i] >= success:
            j += 1
        ans[i] = j
    return ans
```

   `([5,1,3], [1,2,3,4,5], 7)` → `[4, 0, 3]`。主要成本仍是两个排序，`O(n log n + m log m)`。
2. **小值域计数**：`suffix[v]` 表示不小于 `v` 的药水个数（值域 `V = 10^5`，一次后缀累加得到）。每个咒语的下限 `need = -(-success // s)`，`need > V` 时答案 `0`，否则 `suffix[need]`：

```python
def successful_pairs_counting(spells: list[int], potions: list[int], success: int, top: int = 10**5) -> list[int]:
    suffix = [0] * (top + 2)
    for p in potions:
        suffix[p] += 1
    for v in range(top - 1, -1, -1):
        suffix[v] += suffix[v + 1]
    return [suffix[need] if (need := -(-success // s)) <= top else 0 for s in spells]
```

   同样得到 `[4, 0, 3]` 与 `[2, 0, 2]`，总 `O(n + m + V)`，每个咒语 `O(1)`。
3. **药水动态增加**：不能再排序一次了。值域小用树状数组（Fenwick Tree）按值计数，单次增加与前缀查询都是 `O(log V)`；值域大用 `sortedcontainers.SortedList` 之类的有序结构。

**Python 提醒**：`-(-a // b)` 是整数向上取整的惯用写法，等价于 `ceil(a / b)` 但不经过浮点；`:=`（海象运算符）在列表推导的条件表达式里绑定 `need`，只在同一表达式内使用。
