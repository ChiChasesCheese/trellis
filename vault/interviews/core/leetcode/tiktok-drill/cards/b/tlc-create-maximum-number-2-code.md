---
id: tlc-create-maximum-number-2-code
node: b.create-maximum-number
type: qa
step: 2
---
## Q
**LC 321 拼接最大数**｜写出 Python 实现

两个数字数组（长度 `1..500`，元素 0 到 9），共取 `k` 个（`1 <= k <= m + n`）拼成最大的数，同一数组内保持相对顺序，返回各位数组。

## A
**思路。** 对每个可行的 `i`，`pick(nums1, i)` 和 `pick(nums2, k - i)` 用单调栈挑出各自的最大子序列，`merge` 每步比较两边剩余后缀取更大的首位，所有候选取最大值。

```python
def max_number(nums1: list[int], nums2: list[int], k: int) -> list[int]:
    def pick(nums: list[int], t: int) -> list[int]:
        """按原顺序从 nums 里挑 t 个数字，组成最大的子序列（单调栈）。"""
        drop = len(nums) - t                 # 最多还能丢掉几个
        stack: list[int] = []
        for x in nums:
            while drop and stack and stack[-1] < x:   # 栈顶比 x 小又还能丢：丢掉它
                stack.pop()
                drop -= 1
            stack.append(x)
        return stack[:t]                     # 没丢够的部分从尾部截掉

    def merge(a: list[int], b: list[int]) -> list[int]:
        """把两个子序列合并成最大的序列：每步取「剩余后缀」字典序更大的那一边的首位。"""
        out: list[int] = []
        i = j = 0
        while i < len(a) or j < len(b):
            if a[i:] >= b[j:]:               # 比较整个后缀，首位相同时才选得对
                out.append(a[i])
                i += 1
            else:
                out.append(b[j])
                j += 1
        return out

    m, n = len(nums1), len(nums2)
    return max(                              # 等长列表按字典序比较，就是按数值比较
        merge(pick(nums1, i), pick(nums2, k - i))
        for i in range(max(0, k - n), min(k, m) + 1)
    )
```

运行：`[3,4,6,5]`, `[9,1,2,5,8,3]`, `k = 5` → `[9,8,6,5,3]`；`[6,7]`, `[6,0,4]`, `5` → `[6,7,6,0,4]`；`[3,9]`, `[8,9]`, `3` → `[9,8,9]`；`[2,5]`, `[2,6]`, `4` → `[2,6,2,5]`；`[6]`, `[6,7]`, `3` → `[6,7,6]`。

**复杂度。** 外层枚举 `i` 至多 `k + 1` 种；`pick` 是 `O(m + n)`；`merge` 走 `k` 步，每步后缀比较最坏 `O(k)`。总时间最坏 `O(k · (m + n + k^2))`，后缀比较通常在第一个不同的位置就结束，`m = n = 500` 时远低于这个上界。空间 `O(m + n)`。

**写法要点。** Python 列表比较就是字典序比较，`a[i:] >= b[j:]` 一行完成后缀比较，而且「较短且是前缀」的一边更小（`[6] < [6, 7]`），正好符合合并规则；`max(生成器)` 直接在等长候选里取最大，不需要转成整数；`stack[:t]` 处理「没丢够」时从尾部截断；`while drop and stack and ...` 把三个条件按短路顺序排好，空栈时不会访问 `stack[-1]`。
