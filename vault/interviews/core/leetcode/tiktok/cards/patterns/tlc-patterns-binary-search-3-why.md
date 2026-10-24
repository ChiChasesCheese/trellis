---
id: tlc-patterns-binary-search-3-why
node: patterns.binary-search
type: qa
step: 3
---
## Q
**二分查找（Binary Search）｜正确性：不变量与最常见的初值错误**

`first_true` 的循环不变量是什么？把 `hi` 初值写成 `len(a) - 1` 会错在哪里？

## A
**不变量**：在循环的任何时刻，答案（第一个 `True` 的位置）都在 `[lo, hi]` 内，其中 `hi` 是「已知为 `True` 的位置，或者哨兵 `hi0`」；`lo` 左边的位置全部是 `False`。

- 若 `ok(mid)` 为 `True`：`mid` 是候选，答案在 `[lo, mid]`，令 `hi = mid`。
- 若 `ok(mid)` 为 `False`：由单调性，`[lo, mid]` 全是 `False`，答案在 `[mid+1, hi]`，令 `lo = mid + 1`。
- 循环结束时 `lo == hi`，两个界重合，就是答案。

**反例：`hi` 写成 `len(a) - 1`。**

```python
def lower_bound_bad(a: list[int], t: int) -> int:
    lo, hi = 0, len(a) - 1                 # 漏掉了「全部小于 t」这种情况
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < t:
            lo = mid + 1
        else:
            hi = mid
    return lo
print(lower_bound_bad([1, 3, 5], 7))   # 2：指向元素 5，而 5 < 7
```

正确答案是 `3`（插入点在末尾，`bisect_left([1, 3, 5], 7)` 也是 `3`）。`hi` 必须取 `len(a)`，让「所有位置都是 `False`」时有一个落点。

**另一类错误是判定函数不单调**：`ok(x)` 不满足「`False...False True...True`」时，丢掉一半会丢掉真正的答案，而且不会报错，只会给出错误值。
- 写完判定函数后，用 3 个例子验证单调：很小的 `x`、很大的 `x`、临界的 `x`。
