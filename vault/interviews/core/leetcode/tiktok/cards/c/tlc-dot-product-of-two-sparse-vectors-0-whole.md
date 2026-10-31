---
id: tlc-dot-product-of-two-sparse-vectors-0-whole
node: c.dot-product-of-two-sparse-vectors
type: qa
---
## Q
**LC 1570 两个稀疏向量的点积**｜Medium · LC TikTok 全时段热度 26/100

实现类 `SparseVector`：`SparseVector(nums)` 用向量 `nums` 初始化；`dotProduct(vec)` 计算此向量与另一个 `SparseVector` 的点积。稀疏向量是指绝大多数分量为 `0` 的向量，需要高效地存储它并计算点积。进阶：当只有一个向量是稀疏的，怎么办？`n == nums1.length == nums2.length`，`1 <= n <= 10^5`，`0 <= nums1[i], nums2[i] <= 100`。例：`nums1 = [1,0,0,2,3], nums2 = [0,3,0,4,0]` → `8`；`nums1 = [0,1,0,0,0], nums2 = [0,0,0,0,2]` → `0`；`nums1 = [0,1,0,0,2,0,0], nums2 = [1,0,0,0,3,0,4]` → `6`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 只存非零分量（`下标 -> 值` 的字典），点积时遍历非零更少的那个向量，到另一个字典里查同一下标。

**识别。** 「稀疏」意味着存储和计算都应该只与非零个数有关，而不是与长度 `n` 有关；字典查下标是 `O(1)`。

**推导。** 暴力：两个长 `n` 的数组逐位相乘，`O(n)` 时间和空间，完全没利用稀疏。洞察：乘积非零当且仅当两边下标都非零，所以只需要枚举其中一个向量的非零下标，并在另一个里查；选非零更少的那个遍历，代价是 `min(L1, L2)`。

```python
class SparseVector:
    def __init__(self, nums: list[int]) -> None:
        self.nonzero: dict[int, int] = {i: x for i, x in enumerate(nums) if x}   # 只存非零分量：下标 -> 值

    def dotProduct(self, vec: "SparseVector") -> int:
        small, large = sorted((self.nonzero, vec.nonzero), key=len)   # 遍历非零更少的一个
        return sum(x * large[i] for i, x in small.items() if i in large)   # 只有两边都非零的下标才有贡献
```

运行：三个示例依次得到 `8`、`0`、`6`；全零向量之间的点积为 `0`。

**复杂度。** 构造 `O(n)`（扫描一遍原数组），存储 `O(L)`（`L` 为非零个数）；`dotProduct` 时间 `O(min(L1, L2))`，空间 `O(1)`。

**拓展优化。**
- 进阶：若只有一个向量是稀疏的，另一个是稠密数组，就遍历稀疏向量的非零项，直接用下标取稠密数组的值，`O(L)`。
- 两个都稀疏但大小悬殊时，存成「升序下标列表 + 值列表」，短的逐个走、在长的里二分，`O(L1 log L2)`；两者规模相近时用双指针归并 `O(L1 + L2)`：

```python
from bisect import bisect_left


class SparseVectorPairs:
    def __init__(self, nums: list[int]) -> None:
        self.idx = [i for i, x in enumerate(nums) if x]          # 非零下标，天然升序
        self.val = [x for x in nums if x]

    def dotProduct(self, vec: "SparseVectorPairs") -> int:
        a, b = (self, vec) if len(self.idx) <= len(vec.idx) else (vec, self)
        total = lo = 0
        for i, x in zip(a.idx, a.val):           # 短的逐个走，在长的里二分找同一下标
            lo = bisect_left(b.idx, i, lo)       # lo 只增不减：下标升序，后面的查找从上次位置继续
            if lo == len(b.idx):
                break
            if b.idx[lo] == i:
                total += x * b.val[lo]
        return total
```

**易错点。**
- 遍历较大的向量，在较小的里查：时间变成 `O(max(L1, L2))`，没必要。
- 存储时保留零值：字典大小变成 `n`，失去稀疏的意义；用 `if x` 过滤。
- 访问 `large[i]` 前没判断存在：遍历 `small` 的下标在 `large` 里可能没有，要用 `i in large` 或 `large.get(i, 0)`。

**追问。**
- 向量在线更新某个分量：字典 `O(1)` 更新，置零时删除键。
- 多个向量两两点积：对每个向量建一次字典；也可以建倒排索引（下标 -> 向量列表）一次处理，类似搜索引擎。

**同模式。** LC 311 稀疏矩阵的乘法、LC 986 区间列表的交集、LC 88 合并两个有序数组、LC 349 两个数组的交集、LC 1 两数之和。
