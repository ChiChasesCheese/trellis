---
slug: maximum-strong-pair-xor-ii
---
## Q
**LC 2935 找出强数对的最大异或值 II**｜Hard

整数数组 `nums`。一对数 `(x, y)` 是"强数对"当且仅当 `|x - y| <= min(x, y)`（可以选同一个数两次）。求所有强数对中 `x XOR y` 的最大值。

## A
**一句话。** 排序后条件变成 `y <= 2x`（`x <= y`）：用滑动窗口维护"还能当 `x` 的数"，窗口里的数放在 01 字典树里（带计数，支持删除），对每个 `y` 查询窗口内与它异或最大的数。

```python
def maximum_strong_pair_xor(nums):
    nums.sort()
    L = 20                              # 数值 < 2^20
    trie = [[0, 0, 0]]                  # 子节点0、子节点1、经过次数

    def update(x, d):
        node = 0
        for b in range(L - 1, -1, -1):
            c = (x >> b) & 1
            if not trie[node][c]:
                trie.append([0, 0, 0])
                trie[node][c] = len(trie) - 1
            node = trie[node][c]
            trie[node][2] += d

    def query(x):
        node = res = 0
        for b in range(L - 1, -1, -1):
            c = ((x >> b) & 1) ^ 1      # 想走相反的位
            nxt = trie[node][c]
            if nxt and trie[nxt][2]:
                res |= 1 << b
                node = nxt
            else:
                node = trie[node][c ^ 1]
        return res

    ans = left = 0
    for y in nums:
        update(y, 1)
        while nums[left] * 2 < y:       # 不再是强数对，移出窗口
            update(nums[left], -1)
            left += 1
        ans = max(ans, query(y))
    return ans
```

**复杂度。** 时间 `O(n log M)`，空间 `O(n log M)`。

**易错点。**
- 把 `y` 查询放在加入之前：`(y, y)` 也是强数对，要先加入再查。
- 删除只清节点不减计数：遍历时靠计数判断该子树是否还有数，必须减。
- 条件写成 `y - x <= x` 却忘了排序：滑窗依赖有序。

**追问。**
- 为什么窗口左端单调右移？：`y` 增大后，更早的 `x` 更难满足 `2x >= y`，被淘汰就不会再回来。

**同模式。** LC 421 数组中两个数的最大异或值、LC 3022 给定操作次数内使剩余元素的或值最小
