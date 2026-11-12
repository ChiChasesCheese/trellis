---
slug: dot-product-of-two-sparse-vectors
---
## Q
**LC 1570 两个稀疏向量的点积**｜Medium

实现 `SparseVector(nums)` 与 `dotProduct(vec)`，高效存储绝大多数分量为 `0` 的向量并求点积。

## A
**一句话。** 只存非零分量的 `下标 -> 值` 字典，点积时遍历非零更少的一个，到另一个里查同一下标。

```python
class SparseVector:
    def __init__(self, nums):
        self.nz = {i: x for i, x in enumerate(nums) if x}

    def dotProduct(self, vec):
        a, b = sorted((self.nz, vec.nz), key=len)
        return sum(x * b[i] for i, x in a.items() if i in b)
```

**复杂度。** 时间 构造 `O(n)`，点积 `O(min(L1, L2))`（`L` 为非零个数），空间 `O(L)`。

**易错点。**
- 遍历较大的向量去查较小的：变成 `O(max(L1, L2))`。
- 把零值也存进字典：失去稀疏的意义，用 `if x` 过滤。
- 直接 `b[i]` 不判断存在：`a` 的下标在 `b` 里可能没有，`KeyError`。

**追问。**
- 只有一个向量稀疏怎么办？：遍历稀疏的那个，对稠密数组按下标直接取，`O(L)`。
- 两个向量都有序存成 `(下标, 值)` 列表呢？：双指针归并，`O(L1 + L2)`，也可对较大者二分。

**同模式。** LC 311 稀疏矩阵的乘法、LC 986 区间列表的交集、LC 349 两个数组的交集
