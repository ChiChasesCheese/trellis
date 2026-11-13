---
id: cc-performance-numeric-arrays-dot-and-sparse
node: performance.numeric-arrays
type: qa
---
## Q
Write the dot product of two equal-length vectors. Follow-up: the vectors are 10^6 long but only about 10^3 entries are non-zero. Which representation do you switch to, what does the loop look like, and what does it cost?

## A
**Dense: one `zip` loop, O(n). Sparse: keep only the non-zeros as `{index: value}` and walk the smaller dict, O(min(nnz_a, nnz_b)).**

```python
def dot(a, b):
    assert len(a) == len(b)
    return sum(x * y for x, y in zip(a, b))

def to_sparse(v):
    # keep only non-zeros: {index: value}
    return {i: x for i, x in enumerate(v) if x}

def sparse_dot(a, b):
    if len(a) > len(b):          # walk the smaller dict
        a, b = b, a
    return sum(x * b[i] for i, x in a.items() if i in b)
```

- **The gap.** Dense does 10^6 multiplies even when 99.9% are `0 * x`; sparse does at most 10^3 lookups.
- **Sorted pairs instead of a dict.** If non-zeros arrive as sorted `(index, value)` lists, two pointers give O(nnz_a + nnz_b) with no hashing.
- **Very unequal sizes.** 10 non-zeros against 10^6: walk the small list and `bisect` into the large one, O(10 · log 10^6).
- **Complexity.** Dense O(n) time, O(1) extra; sparse O(min nnz) time, O(nnz) memory.

**Next follow-up: "parallelise it."** Split the index range into chunks, one partial dot per chunk, add the partials. For sparse data split by *number of non-zeros*, not by index range, or one chunk gets all the work.

## Q zh
写出两个等长向量的点积。追问：向量长 10^6，但只有大约 10^3 个非零元素。你换成什么表示？循环长什么样？代价是多少？

## A zh
**稠密：一个 `zip` 循环，O(n)。稀疏：只存非零元素 `{下标: 值}`，遍历较小的那个字典，O(min(nnz_a, nnz_b))。**

```python
def dot(a, b):
    assert len(a) == len(b)
    return sum(x * y for x, y in zip(a, b))

def to_sparse(v):
    # keep only non-zeros: {index: value}
    return {i: x for i, x in enumerate(v) if x}

def sparse_dot(a, b):
    if len(a) > len(b):          # walk the smaller dict
        a, b = b, a
    return sum(x * b[i] for i, x in a.items() if i in b)
```

- **差距。** 稠密版要做 10^6 次乘法，哪怕 99.9% 都是 `0 * x`；稀疏版最多 10^3 次查找。
- **用有序对代替字典。** 如果非零元素本来就是按下标排好序的 `(index, value)` 列表，双指针是 O(nnz_a + nnz_b)，完全不用哈希。
- **两边大小悬殊。** 10 个非零对 10^6 个：遍历小的，在大的里 `bisect`，O(10 · log 10^6)。
- **复杂度。** 稠密 O(n) 时间、O(1) 额外空间；稀疏 O(min nnz) 时间、O(nnz) 内存。

**下一个追问：「把它并行化。」** 把下标区间切块，每块算一个部分点积，最后相加。稀疏数据要按*非零元素个数*切块，而不是按下标区间，否则可能一块拿走全部工作。
