---
id: tlc-tops-partition-array-into-two-arrays-to-minimize-sum-difference-0-whole
node: binary-search.partition-array-into-two-arrays-to-minimize-sum-difference
type: qa
---
## Q
**LC 2035 将数组分成两个数组并最小化数组和的差**｜Hard · 全公司热度第 261 名

给你一个长度为 `2 * n` 的整数数组 `nums`。把它分成两个长度都为 `n` 的数组（每个元素必须放入其中一个），分别求和，使两个数组和之差的**绝对值最小**，返回这个最小值。`1 <= n <= 15`，`nums.length == 2 * n`，`-10^7 <= nums[i] <= 10^7`。例：`nums = [3,9,7,3]` → `2`（`[3,9]` 与 `[7,3]`）；`nums = [-36,36]` → `72`；`nums = [2,-1,0,4,-2,-9]` → `0`（`[2,4,-9]` 与 `[-1,0,-2]`）。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 折半枚举（meet in the middle）+ 按选取个数分组 + 排序后二分查找最接近的值。

**一句话。** 把数组劈成两半各自枚举所有子集的和（按选了几个分组），再让左半选 `c` 个、右半选 `n - c` 个，用二分在右半里找最接近 `总和 / 2` 的搭档。

**识别。** 「恰好各一半」「`n <= 15`、总长 `30`」「值可负、范围大」：`C(30, 15)` 约 `1.55 * 10^8` 太大，`2^30` 更大；值域大又含负数，背包 DP 的状态数撑不住。长度 `30` 正是折半枚举的信号：两半各 `2^15 = 32768`。

**推导。** 设总和 `S`，选出的那半和为 `x`，差为 `|S - 2x|`，目标是 `x` 尽量靠近 `S / 2`。直接枚举 `C(2n, n)` 种选法太多。把数组劈成两半，从前半选 `c` 个、后半选 `n - c` 个，`x = a + b`：对前半的每个和 `a`，要在后半"恰好选 `n - c` 个"的和里找离 `S/2 - a` 最近的 `b`，后半的和排序后二分，答案只可能是插入位置左右两个相邻值。

```python
from bisect import bisect_right
from math import inf


def minimum_difference(nums: list[int]) -> int:
    n = len(nums) // 2
    total = sum(nums)

    def sums_by_size(arr: list[int]) -> list[list[int]]:
        by = [[0]] + [[] for _ in arr]  # by[c]：恰好选 c 个元素时所有可能的和
        for x in arr:
            for c in range(len(arr) - 1, -1, -1):  # c 从大到小：每个元素只被用一次
                by[c + 1] += [s + x for s in by[c]]
        return by

    left, right = sums_by_size(nums[:n]), sums_by_size(nums[n:])
    best = inf
    for c in range(n + 1):  # 前半选 c 个，后半就必须选 n - c 个
        rs = sorted(right[n - c])
        for a in left[c]:
            # 想让 a + b 最接近 total / 2：b 最接近 total // 2 - a，只看二分位置左右两个邻居
            i = bisect_right(rs, total // 2 - a)
            for b in rs[max(i - 1, 0):i + 1]:
                best = min(best, abs(total - 2 * (a + b)))
    return best
```

运行：`[3,9,7,3]` → `2`；`[-36,36]` → `72`；`[2,-1,0,4,-2,-9]` → `0`；`[5,5]` → `0`；`[1,1,1,3]` → `2`。`n = 15`（长度 `30`）的随机输入同样瞬间完成。

**复杂度。** 时间 `O(2^n * n)`（两半各 `2^n` 个子集，排序与二分带 `log`），空间 `O(2^n)`。

**拓展优化。**
- 排好序之后，左半的和 `left[c]` 也排序，用双指针代替二分，去掉二分的 `log`；常数更小，写法更绕，二分已够通过。

**易错点。**
- 忽略"各 `n` 个"，只找最接近 `S/2` 的任意子集：`[1,1,1,3]` 得到 `0`（单独取 `3`），正确是 `2`，因为取 `3` 的那半只有一个元素。所以必须按选取个数分组。
- 初始最优值写成 `abs(total)`：它不一定对应一种合法分法，`[6,-1,6,-13]` 会返回 `2`，正确是 `12`；用 `inf`。
- 暴力 `itertools.combinations(nums, n)` 在 `n = 15` 时有约 `1.55 * 10^8` 种，超时；折半枚举只枚举两个 `2^15`。

**同模式。** LC 1755 最接近目标值的子序列和、LC 416 分割等和子集、LC 1049 最后一块石头的重量 II、LC 805 数组的均值分割。
