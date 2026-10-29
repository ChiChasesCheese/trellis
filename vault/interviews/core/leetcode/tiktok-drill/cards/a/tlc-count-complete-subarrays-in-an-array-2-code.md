---
id: tlc-count-complete-subarrays-in-an-array-2-code
node: a.count-complete-subarrays-in-an-array
type: qa
step: 2
---
## Q
**LC 2799 统计完全子数组的数目**｜写出 Python 实现

正整数数组 `nums`（长度 `1..1000`，元素 `1..2000`）。不同元素个数等于整个数组不同元素个数的连续子数组称为完全子数组。返回完全子数组的数目。

## A
**思路。** 用 `Counter` 维护窗口 `nums[left:right]`。对每个 `left`，右指针向右扩到窗口种类数达到 `total`；此时以 `left` 开头的合法子数组数是 `n - right + 1`。然后把 `nums[left]` 移出窗口，进入下一个 `left`。

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

**复杂度。** 时间 `O(n)`：每个下标最多被 `right` 加入一次、被 `left` 移出一次；空间 `O(k)`，`k` 为不同元素个数。

**写法要点。** `len(set(nums))` 一步得到 `total`；`Counter` 对不存在的键读写默认 `0`，`cnt[x] += 1` 不用判断；`len(cnt)` 就是窗口里的种类数，前提是计数归零时 `del` 掉键；`right` 定义成开区间端点，窗口是 `nums[left:right]`，和 Python 切片一致，计数公式 `n - right + 1` 不容易错位。
