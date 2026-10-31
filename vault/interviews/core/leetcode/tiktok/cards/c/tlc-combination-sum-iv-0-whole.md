---
id: tlc-combination-sum-iv-0-whole
node: c.combination-sum-iv
type: qa
---
## Q
**LC 377 组合总和 Ⅳ**｜Medium · LC TikTok 全时段热度 25/100 · CodeTop 国内累计 3 次 · 最近 2022-08-03（国内 CodeTop）

给定由不同正整数组成的数组 `nums` 和目标整数 `target`，返回从 `nums` 中选数（可重复使用）使总和为 `target` 的元素组合个数，顺序不同的序列算不同的组合。题目保证答案在 32 位整数范围内。`1 <= nums.length <= 200`，`1 <= nums[i] <= 1000`，`nums` 中元素互不相同，`1 <= target <= 1000`。例：`nums = [1,2,3], target = 4` → `7`（`1+1+1+1`、`1+1+2`、`1+2+1`、`1+3`、`2+1+1`、`2+2`、`3+1`）；`nums = [9], target = 3` → `0`。进阶：数组含负数会发生什么？需要加什么限制？

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** `dp[t]` 是和为 `t` 的有序序列个数，`dp[t] = Σ dp[t - x]`（枚举最后一个数 `x`），外层循环是目标和、内层循环是数。

**识别。** 「顺序不同算不同」是排列计数（背包问题里的「排列数」）；与 LC 518 零钱兑换 II（组合数，顺序无关）只差循环顺序。

**推导。** 暴力：递归枚举每一步选哪个数，`O(|nums|^target)`。浪费：和为 `t - x` 的子问题被重复求解。洞察：序列的最后一个数是 `x` 时，前面是任意一个和为 `t - x` 的序列，所以 `dp[t]` 等于各 `dp[t - x]` 之和；`dp[0] = 1` 表示空序列。

```python
def combination_sum4(nums: list[int], target: int) -> int:
    dp = [0] * (target + 1)                      # dp[t]：和为 t 的有序序列个数
    dp[0] = 1                                    # 空序列：和为 0 只有一种
    for t in range(1, target + 1):               # 外层枚举目标和，内层枚举最后一个数 -> 顺序不同算不同序列
        for x in nums:
            if x <= t:
                dp[t] += dp[t - x]               # 以 x 结尾的序列数 = 和为 t-x 的序列数
    return dp[target]
```

运行：`[1,2,3]`, `4` → `7`；`[9]`, `3` → `0`；`[1]`, `1000` → `1`；`[1,2,3]`, `1` → `1`。

**复杂度。** 时间 `O(target * |nums|)`，空间 `O(target)`。

**拓展优化。**
- 进阶（含负数）：序列可以无限延伸（如 `[1, -1]` 凑 `0` 有无穷多种），必须限制序列长度（或禁止某类组合）；限制长度 `L` 时按长度逐层推进，状态是「当前和 -> 个数」：

```python
from collections import defaultdict


def combination_sum4_with_negatives(nums: list[int], target: int, max_len: int) -> int:
    ways: dict[int, int] = {0: 1}                # ways[s]：当前长度的序列里，和为 s 的个数
    total = 0
    for _ in range(max_len):                     # 有负数时必须限制序列长度，否则个数可能无限
        nxt: defaultdict[int, int] = defaultdict(int)
        for s, c in ways.items():
            for x in nums:
                nxt[s + x] += c
        ways = nxt
        total += ways.get(target, 0)             # 长度 1..max_len 各自累加
    return total
```

**易错点。**
- 两层循环顺序写反（先数后目标）：这样得到的是不计顺序的组合数，`[1,2,3]`, `4` 会得到 `4` 而不是 `7`。
- `dp[0]` 初值写成 `0`：整个表恒为 `0`。
- 不判断 `x <= t`：`t - x` 为负时 Python 的负下标会读到数组末尾，结果错误。

**追问。**
- 每个数只能用一次（不可重复）、顺序无关：回到 0-1 背包，LC 40 组合总和 II。
- 输出所有序列而不只是个数：回溯，规模指数级。

**同模式。** LC 518 零钱兑换 II、LC 322 零钱兑换、LC 70 爬楼梯、LC 39 组合总和、LC 279 完全平方数。
