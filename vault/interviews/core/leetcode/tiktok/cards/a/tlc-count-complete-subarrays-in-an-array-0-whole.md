---
id: tlc-count-complete-subarrays-in-an-array-0-whole
node: a.count-complete-subarrays-in-an-array
type: qa
---
## Q
**LC 2799 统计完全子数组的数目**｜Medium · LC TikTok 热度 62/100

给一个正整数数组 `nums`。如果某个子数组里**不同元素的个数**等于整个数组不同元素的个数，就称它是完全子数组（子数组是连续非空序列）。返回完全子数组的数目。`1 <= nums.length <= 1000`，`1 <= nums[i] <= 2000`。例：`[1,3,1,2,2]` → `4`（`[1,3,1,2]`、`[1,3,1,2,2]`、`[3,1,2]`、`[3,1,2,2]`）；`[5,5,5,5]` → `10`（任意子数组都满足）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 先数出整个数组有 `total` 种不同元素；对每个左端点 `left`，找最小的右端使窗口凑齐 `total` 种，这之后的所有右端点都合法，贡献 `n - right + 1` 个；`left` 右移时这个最小右端只会不动或右移，所以用双指针。`O(n)`。

**识别。** 「子数组 + 不同元素数达到某个值 + 数有多少个」是滑动窗口计数的信号。条件是单调的：窗口向右扩大，不同元素数只增不减，所以「最短合法右端」存在且随 `left` 单调不减。区别于「求最长 / 最短」：这里是**数个数**，每个 `left` 贡献一批，而不是更新一个最优值。`n <= 1000` 时 `O(n^2)` 也能过，面试里先给 `O(n)`。

**推导。** 暴力：枚举所有子数组再数不同元素，`O(n^3)`。改进：固定 `left` 向右扩，用集合累计，凑齐就停并加上 `n - j`，`O(n^2)`。浪费：`left` 变成 `left + 1` 后重新从头扩。洞察：窗口 `[left+1, r]` 若完全，则 `[left, r]` 一定完全，所以最小右端不会回退，`right` 只进不退。最优：两个指针各走一遍。

```python
from collections import Counter


def count_complete_subarrays(nums: list[int]) -> int:
    n, total = len(nums), len(set(nums))      # total：整个数组的不同元素数
    cnt: Counter[int] = Counter()             # 窗口 nums[left:right] 内每个数的出现次数
    ans = right = 0
    for left in range(n):
        while right < n and len(cnt) < total:   # 扩右：直到窗口凑齐 total 种数
            cnt[nums[right]] += 1
            right += 1
        if len(cnt) < total:                    # 到末尾也凑不齐：更大的 left 更不可能
            break
        ans += n - right + 1                    # 以 left 开头、右端点在 [right-1, n-1] 的子数组都完全
        cnt[nums[left]] -= 1                    # 缩左：left 出窗口
        if cnt[nums[left]] == 0:
            del cnt[nums[left]]                 # 计数归零必须删键，否则 len(cnt) 会虚高
    return ans
```

**运行。** `[1,3,1,2,2]` → `4`；`[5,5,5,5]` → `10`；`[7]` → `1`；`[1,2,3]` → `1`；`[1,2,1,2]` → `6`。

**复杂度。** 时间 `O(n)`：`left` 和 `right` 各只前进 `n` 步；空间 `O(k)`，`k` 是不同元素数，最多 `min(n, 2000)`。

**易错点。**
- 计数减到 `0` 不删键：`Counter` 里留着值为 `0` 的键，`len(cnt)` 虚高。`[1,3,1,2,2]` 会算出 `10`，正确是 `4`。
- 区间写法混淆：`right` 是开区间端点（窗口 `nums[left:right]`），所以每个 `left` 贡献 `n - right + 1`；写成 `n - right` 会少算，`[1,3,1,2,2]` 得 `2`。
- 右端扩到末尾仍凑不齐时必须 `break`：不 break 就会对不完全的窗口也执行 `ans += n - right + 1`，每个剩余的 `left` 白白多加 `1`。

**追问。**
- 恰好 `k` 种不同元素的子数组数（LC 992）：`atMost(k) - atMost(k - 1)`，每个 `atMost` 都是一遍滑动窗口。
- 求最短的完全子数组：同样的窗口，每次凑齐时用 `right - left` 更新最小值。
- 输入是流，或值域特别大：`Counter` 换成普通 `dict` 即可，窗口逻辑不变；但需要能回看左端，得保留窗口内的元素。

**同模式。** LC 992 K 个不同整数的子数组、LC 3 无重复字符的最长子串、LC 930 和相同的二元子数组、LC 1248 统计优美子数组、LC 713 乘积小于 K 的子数组。
