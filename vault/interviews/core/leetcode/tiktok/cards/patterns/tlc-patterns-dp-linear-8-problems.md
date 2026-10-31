---
id: tlc-patterns-dp-linear-8-problems
node: patterns.dp-linear
type: qa
step: 8
---
## Q
**动态规划：线性与状态机｜本组用到线性 DP 的题**

按变形分类，这个题组里哪些题属于线性 DP 或状态机？

## A
**一维递推**
- LC 70 爬楼梯
- LC 198 打家劫舍
- LC 53 最大子数组和
- LC 1997 访问完所有房间的第一天
- LC 746 使用最小花费爬楼梯（高频）

**状态机**
- LC 121 买卖股票的最佳时机
- LC 122 买卖股票的最佳时机 II

**分段**
- LC 1043 分隔数组以得到最大和
- LC 139 单词拆分（高频）

**以谁结尾 / 带最后一步**
- LC 300 最长递增子序列
- LC 403 青蛙过河
- LC 678 有效的括号字符串（状态：未匹配左括号的可能区间）
- LC 1048 最长字符串链（高频）
- LC 1691 堆叠长方体的最大高度（高频）

**可以用 DP 也可以用贪心**
- LC 55 跳跃游戏
- LC 45 跳跃游戏 II

提示：先写一句话定义 `dp[i]`，再写转移、初值、遍历顺序；能压成两三个变量就压。

**例题：** LC 70 爬楼梯

每次爬 `1` 或 `2` 阶，爬到第 `n` 阶有多少种不同方法。`1 <= n <= 45`。

```python
def climb_stairs(n: int) -> int:
    prev, cur = 1, 1                   # f(0) = 1（站着不动算一种），f(1) = 1
    for _ in range(n - 1):
        prev, cur = cur, prev + cur    # f(k) = f(k-1) + f(k-2)：最后一步迈 1 阶或 2 阶
    return cur
```

**例题：** LC 198 打家劫舍

一排房屋，`nums[i]` 是第 `i` 间的现金，不能偷相邻的两间，求最多能偷多少。`1 <= nums.length <= 100`，`0 <= nums[i] <= 400`。

```python
def rob(nums: list[int]) -> int:
    skip = take = 0                         # skip：不偷当前房的最优；take：偷当前房的最优
    for x in nums:
        skip, take = max(skip, take), skip + x
    return max(skip, take)
```

**例题：** LC 53 最大子数组和

求整数数组 `nums` 中和最大的非空连续子数组，返回其和。`1 <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`。

```python
from itertools import islice
def max_sub_array(nums: list[int]) -> int:
    best = cur = nums[0]                # cur：以当前元素结尾的最大子数组和
    for x in islice(nums, 1, None):     # 跳过首元素，又不拷贝切片
        cur = max(x, cur + x)           # 接在前面后面，或者从 x 重新开始
        best = max(best, cur)
    return best
```

**例题：** LC 1997 访问完所有房间的第一天

`n` 个房间，第 `0` 天在房间 `0`。若今天访问房间 `i` 后，累计访问它的次数为奇数，次日去 `nextVisit[i]`，为偶数则去 `(i + 1) mod n`。返回第一次访问完所有房间的日期，对 `10^9 + 7` 取余。`2 <= n <= 10^5`，`0 <= nextVisit[i] <= i`。

```python
def first_day_been_in_all_rooms(next_visit: list[int]) -> int:
    mod = 10**9 + 7
    n = len(next_visit)
    first = [0] * n                                # first[i] = 第一次到达房间 i 的日期
    for i in range(n - 1):
        # 第一次到 i（奇数次）-> 回到 nv = next_visit[i]，再走回 i 的时间是 first[i] - first[nv]
        # 第二次到 i（偶数次）-> 第二天去 i+1
        first[i + 1] = (2 * first[i] - first[next_visit[i]] + 2) % mod
    return first[-1]
```

**例题：** LC 121 买卖股票的最佳时机

`prices[i]` 是第 `i` 天的股价，只能买一次、卖一次（先买后卖），求最大利润，不能获利返回 `0`。`1 <= prices.length <= 10^5`。

```python
def max_profit(prices: list[int]) -> int:
    low, best = prices[0], 0          # low：迄今最低价
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best
```

**例题：** LC 122 买卖股票的最佳时机 II

`prices[i]` 是第 `i` 天的股价，可以多次买卖，任何时候最多持有一股，求最大利润。`1 <= prices.length <= 3 * 10^4`，`0 <= prices[i] <= 10^4`。

```python
def max_profit(prices: list[int]) -> int:
    # 每一段上涨都能吃到：把所有 “后一天比前一天高” 的差额加起来
    return sum(max(today - yesterday, 0) for yesterday, today in pairwise(prices))
```

**例题：** LC 1043 分隔数组以得到最大和

把数组 `arr` 分成若干连续段，每段长度至多 `k`，每段的所有元素都变成该段最大值，求变换后元素和的最大值。`1 <= arr.length <= 500`，`0 <= arr[i] <= 10^9`，`1 <= k <= arr.length`。

```python
def max_sum_after_partitioning(arr: list[int], k: int) -> int:
    n = len(arr)
    dp = [0] * (n + 1)                  # dp[i]：前 i 个元素分隔后的最大和
    for i in range(1, n + 1):
        seg_max = 0
        for length in range(1, min(k, i) + 1):    # 枚举最后一段的长度
            seg_max = max(seg_max, arr[i - length])   # 滚动维护这一段的最大值
            dp[i] = max(dp[i], dp[i - length] + seg_max * length)
    return dp[n]
```

**例题：** LC 300 最长递增子序列

求整数数组 `nums` 的最长严格递增子序列的长度（子序列不要求连续）。`1 <= nums.length <= 2500`，`-10^4 <= nums[i] <= 10^4`。

```python
from bisect import bisect_left
def length_of_lis(nums: list[int]) -> int:
    tails: list[int] = []                          # tails[k] = 长度为 k+1 的递增子序列的最小结尾
    for x in nums:
        i = bisect_left(tails, x)                  # 严格递增：第一个 >= x 的位置
        if i == len(tails):
            tails.append(x)                        # x 比所有结尾都大：最长长度 +1
        else:
            tails[i] = x                           # 让长度 i+1 的结尾变得更小，对后面更有利
    return len(tails)
```

**例题：** LC 403 青蛙过河

升序石子位置 `stones`，青蛙从位置 `0` 出发，第一步只能跳 `1`；上一步跳 `k`，下一步只能跳 `k - 1`、`k` 或 `k + 1`，只能落在石子上。判断能否到达最后一块石子。`2 <= stones.length <= 2000`，`stones[0] == 0`。

```python
def can_cross(stones: list[int]) -> bool:
    jumps: dict[int, set[int]] = {pos: set() for pos in stones}   # 石子位置 -> 能以哪些「最后一跳长度」站上来
    jumps[0].add(0)                            # 起点：当作上一跳长度 0，于是下一跳只能是 1
    for pos in stones:
        for k in jumps[pos]:
            for step in (k - 1, k, k + 1):
                if step > 0 and pos + step in jumps:
                    jumps[pos + step].add(step)
    return bool(jumps[stones[-1]])
```

**例题：** LC 678 有效的括号字符串

字符串 `s` 只含 `'('`、`')'`、`'*'`，其中 `'*'` 可当作 `'('`、`')'` 或空串，判断 `s` 能否是有效括号串。`1 <= s.length <= 100`。

```python
def check_valid_string(s: str) -> bool:
    lo = hi = 0                        # 还没配对的 '(' 数量的可能区间 [lo, hi]
    for ch in s:
        lo += 1 if ch == '(' else -1   # '*' 当 ')' 或 ')' 都让 lo 减一
        hi += 1 if ch != ')' else -1   # '*' 当 '(' 或 '(' 都让 hi 加一
        if hi < 0:                     # 即使全当 '(' 也配不上这个 ')'
            return False
        lo = max(lo, 0)                # 区间下界不能为负：多出来的 '*' 当空串
    return lo == 0                     # 0 在区间里，说明存在一种取法恰好配平
```

**例题：** LC 55 跳跃游戏

`nums[i]` 是在下标 `i` 最多能向前跳的长度，从下标 `0` 出发，判断能否到达最后一个下标。`1 <= nums.length <= 10^4`，`0 <= nums[i] <= 10^5`。

```python
def can_jump(nums: list[int]) -> bool:
    reach = 0                               # 目前能到达的最远下标
    for i, step in enumerate(nums):
        if i > reach:
            return False                    # 连 i 都够不着，后面更不可能
        reach = max(reach, i + step)
    return True
```

**例题：** LC 45 跳跃游戏 II

`nums[i]` 是在下标 `i` 最多能向前跳的长度，求从下标 `0` 到最后一个下标的最少跳跃次数（保证能到达）。`1 <= nums.length <= 10^4`，`0 <= nums[i] <= 1000`。

```python
def jump(nums: list[int]) -> int:
    jumps = cur_end = farthest = 0
    for i in range(len(nums) - 1):      # 最后一格不用再跳，所以不扫它
        farthest = max(farthest, i + nums[i])
        if i == cur_end:                # 当前这一跳的范围走完了，必须再跳一次
            jumps += 1
            cur_end = farthest          # 下一层的右边界
    return jumps
```

**例题：** LC 746 使用最小花费爬楼梯

整数数组 `cost`，`cost[i]` 是从第 `i` 级台阶向上爬需要支付的费用。支付后可以向上爬**一级或两级**。你可以选择从下标 `0` 或下标 `1` 的台阶出发。返回到达楼梯顶部（下标 `cost.length`，最后一级之后的位置）的最低总花费。`2 <= cost.length <= 1000`，`0 <= cost[i] <= 999`。

```python
def min_cost_climbing_stairs(cost: list[int]) -> int:
    two_back = one_back = 0                    # 到达第 i-2、i-1 级的最小花费；起点 0、1 都免费
    for i in range(2, len(cost) + 1):
        two_back, one_back = one_back, min(one_back + cost[i - 1], two_back + cost[i - 2])
    return one_back
```

**例题：** LC 139 单词拆分

给字符串 `s` 和字符串列表 `wordDict`（字典）。如果能用字典里的一个或多个单词拼接出 `s` 就返回 `true`；单词可以重复使用，也不要求用完字典。`1 <= s.length <= 300`，`1 <= wordDict.length <= 1000`，`1 <= wordDict[i].length <= 20`，`s` 和单词都只含小写字母，字典里的单词互不相同。

```python
def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)                       # 哈希集合：判断"切片是不是单词"是 O(L)
    max_len = max(map(len, words))               # 单词最长 max_len，更长的切片不用试
    dp = [True] + [False] * len(s)               # dp[i]：前 i 个字符 s[:i] 能否被拆成单词
    for i in range(1, len(s) + 1):
        dp[i] = any(dp[j] and s[j:i] in words for j in range(max(0, i - max_len), i))
    return dp[-1]
```

**例题：** LC 1048 最长字符串链

给单词数组 `words`，每个单词由小写字母组成。如果可以在 `wordA` 的**任意位置**添加**恰好一个**字母（不改变其他字符的相对顺序）得到 `wordB`，就说 `wordA` 是 `wordB` 的**前身**，例如 `"abc"` 是 `"abac"` 的前身，`"cba"` 不是 `"bcad"` 的前身。**词链**是单词序列 `[word_1, ..., word_k]`（`k >= 1`），其中每个单词是下一个的前身；单个单词本身就是长度为 `1` 的词链。返回从 `words` 里选词能组成的最长词链的长度。`1 <= words.length <= 1000`，`1 <= words[i].length <= 16`。

```python
def longest_str_chain(words: list[str]) -> int:
    dp: dict[str, int] = {}                                  # dp[w]：以 w 结尾的最长词链
    for w in sorted(words, key=len):                         # 短的先处理，前身一定已算好
        dp[w] = 1 + max((dp.get(w[:i] + w[i + 1:], 0) for i in range(len(w))), default=0)
    return max(dp.values())
```

**例题：** LC 1691 堆叠长方体的最大高度

给 `n` 个长方体，`cuboids[i] = [width, length, height]`。从中选一个**子集**堆叠起来：长方体 `i` 能放在 `j` 上，当且仅当 `width_i <= width_j`、`length_i <= length_j`、`height_i <= height_j`；每个长方体可以任意旋转（重新排列长宽高）后再放。返回堆叠后的**最大高度**。`1 <= n <= 100`，`1 <= width_i, length_i, height_i <= 100`。

```python
def max_height(cuboids: list[list[int]]) -> int:
    boxes = sorted(sorted(c) for c in cuboids)      # 先让每个长方体 w<=l<=h，再整体按字典序排
    dp = [0] * len(boxes)                            # dp[i]：以 boxes[i] 为底的最大高度
    for i, box in enumerate(boxes):
        dp[i] = box[2] + max(
            (dp[j] for j in range(i) if all(a <= b for a, b in zip(boxes[j], box))),
            default=0,                               # 上面放不了任何箱子：只有它自己
        )
    return max(dp)
```
