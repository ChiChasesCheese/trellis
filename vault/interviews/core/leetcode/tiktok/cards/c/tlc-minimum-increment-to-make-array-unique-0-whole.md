---
id: tlc-minimum-increment-to-make-array-unique-0-whole
node: c.minimum-increment-to-make-array-unique
type: qa
---
## Q
**LC 945 使数组唯一的最小增量操作**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 1 次 · 最近 2022-05-20（国内 CodeTop）

给你一个整数数组 `nums`。每次 `move` 操作选择任意下标 `i`，把 `nums[i]` 加 1。返回使 `nums` 中每个值都唯一所需的最少操作次数。保证答案在 32 位整数范围内。`1 <= nums.length <= 10^5`，`0 <= nums[i] <= 10^5`。例：`nums = [1,2,2]` → `1`（变成 `[1,2,3]`）；`nums = [3,2,1,2,1,7]` → `6`（变成 `[3,4,1,2,5,7]`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 排序后从小到大扫描，每个数至少要比前一个数大 1，不够就抬到「前一个数 + 1」，抬了多少就加多少次操作，`O(n log n)`。

**识别。** 「只能增大、要求互不相同、操作数最少」：增大的方向固定，排序后每个数只和前一个有关，贪心成立。值域只有 `10^5`，也提示可以用计数数组把排序省掉。

**推导。** 暴力：每个重复数一格一格加 1，直到撞不上已用的值，最坏全是同一个数时 `O(n²)`。洞察：最终的互不相同序列，排序后一定严格递增；把小的数留在原地、重复的往后让，总代价最小。所以排序后维护「下一个可用的最小值」`nxt`：当前数 `x` 取 `max(x, nxt)`，代价 `max(x, nxt) - x`，然后 `nxt` 变成它加 1。

```python
def min_increment_for_unique(nums: list[int]) -> int:
    moves = 0
    nxt = 0                                      # 下一个还没被占用的最小值
    for x in sorted(nums):                       # 升序处理：小的数先占位
        target = max(x, nxt)                     # 比 nxt 小的数必须抬到 nxt，否则留在原地
        moves += target - x
        nxt = target + 1
    return moves
```

运行：`[1,2,2]` → `1`，`[3,2,1,2,1,7]` → `6`；`[5]` → `0`，`[7,7,7,7]` → `6`，`[0] * 100000` → `4999950000`。

**复杂度。** 时间 `O(n log n)`（排序），空间 `O(n)`（`sorted` 的副本）。

**拓展优化。**
- 计数数组把排序去掉，`O(n + V)`（`V` 为值域）：从小到大扫值，多余的重复数「顺延」到下一个值，顺延的个数就是该步的代价。

```python
def min_increment_for_unique_counting(nums: list[int]) -> int:
    top = max(nums) + len(nums)                  # 最终最大值不超过 max + n
    cnt = [0] * (top + 1)
    for x in nums:
        cnt[x] += 1
    moves = carry = 0                            # carry：从前面顺延过来、还没落座的数
    for v in range(top + 1):
        carry += cnt[v]
        if carry:
            carry -= 1                           # 一个数落在 v
        moves += carry                           # 其余的都得再往后挪一格
    return moves
```

**易错点。**
- 不排序直接用 `nxt` 贪心：`[3,2,1,2,1,7]` 得到 `17`，正确是 `6`。
- `nxt` 更新成 `x + 1` 而不是 `target + 1`：`[1,1,1]` 得到 `2`，正确是 `3`。
- 总操作数用 `int` 没问题，Java / C++ 里全相同时约 `5 * 10^9`，要用 64 位整数。

**追问。**
- 同时允许加和减、总代价是 `|变化量|`：这是斜率技巧（slope trick）的题，用大根堆维护。
- 只要判断能否在 `k` 次内完成：算出最小次数与 `k` 比较即可。

**同模式。** LC 1827 最少操作使数组递增、LC 1647 字符频次唯一的最小删除次数、LC 135 分发糖果、LC 1005 K 次取反后最大化的数组和、LC 2310 个位数字为 K 的整数之和。
