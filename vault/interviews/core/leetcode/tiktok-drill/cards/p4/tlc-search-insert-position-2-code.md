---
id: tlc-search-insert-position-2-code
node: p4.search-insert-position
type: qa
step: 2
---
## Q
**LC 35 搜索插入位置**｜写出 Python 实现

升序、无重复元素的整数数组 `nums`（`1 <= len <= 10^4`，取值 `-10^4` 到 `10^4`）和 `target`（同范围）。找到 `target` 返回下标，否则返回它按顺序应插入的下标，`O(log n)`。

## A
**思路。** 在半开区间 `[lo, hi)` 里找第一个 `>= target` 的位置，`hi` 从 `len(nums)` 开始，因为插到末尾也是合法答案。中点小于 `target`，丢掉左半含中点；否则保留中点，丢掉右半。

```python
def search_insert(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums)                    # 答案区间 [lo, hi]，hi 可以等于 len(nums)（插到末尾）
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1                     # mid 和它左边都 < target，答案在右边
        else:
            hi = mid                         # mid 可能就是答案，保留
    return lo
```

运行：`([1,3,5,6], 5)` → `2`，`([1,3,5,6], 2)` → `1`，`([1,3,5,6], 7)` → `4`，`([1,3,5,6], 0)` → `0`，`([1], 1)` → `0`；对 `bisect.bisect_left` 的结果逐一相同。

**复杂度。** 时间 `O(log n)`（每轮区间减半），空间 `O(1)`。

**写法要点。**
- 面试里先手写，让面试官看到你对边界的掌握；写完可以补一句 `bisect_left(nums, target)` 是标准库的同一个函数。
- Python 的整数不会溢出，`(lo + hi) // 2` 没问题；用 C++ 或 Java 要写 `lo + (hi - lo) // 2`。
- 循环不变量：`nums[:lo]` 全部 `< target`，`nums[hi:]` 全部 `>= target`；循环结束时 `lo == hi`，两段拼起来正好是整个数组，边界就是答案。
- `bisect_left(range(a, b), True, key=pred)`（3.10+）可以把「某个单调判定函数的第一个真值」直接交给标准库，适用于不是数组的答案空间。
