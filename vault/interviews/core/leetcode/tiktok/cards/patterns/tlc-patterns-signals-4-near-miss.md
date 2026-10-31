---
id: tlc-patterns-signals-4-near-miss
node: patterns.signals
type: qa
step: 4
---
## Q
**模式识别｜长得像、其实要换算法的近似信号**

哪些题面信号看上去指向 A 模式，实际上必须用 B？举出最容易选错的几组。

## A
| 看起来像 | 实际要 | 为什么 |
|---|---|---|
| 子数组和 = `k`，用滑动窗口 | 前缀和 + 哈希 | 数组含**负数**时，窗口右扩和不单调（LC 560）；全正数才能滑动窗口（LC 209）（例：LC 560 和为 K 的子数组） |
| 求最少硬币，贪心取最大面额 | DP | 局部最优不推出全局：硬币 `[1, 3, 4]` 凑 `6`，贪心是 `4+1+1` 三枚，最优 `3+3` 两枚（例：LC 322 零钱兑换） |
| 子串，用 DP | 滑动窗口 | 子串**连续**、约束单调时，窗口 `O(n)`，DP 不必要（例：LC 3 无重复字符的最长子串） |
| 子序列，用滑动窗口 | DP | 子序列不要求连续，窗口的「收缩」没有意义（例：LC 300 最长递增子序列） |
| 最短路径，用 DFS | BFS（无权）/ Dijkstra（有权） | DFS 先找到的路径不一定最短（例：LC 286 墙与门；高频：LC 127 单词接龙） |
| 无权图最短，用 Dijkstra | BFS | 都能对，BFS `O(V+E)` 更简单；第一个碰到的叶子就是最近的（例：LC 111 二叉树的最小深度；高频：LC 1091 二进制矩阵中的最短路径） |
| 有负权边，用 Dijkstra | Bellman-Ford | Dijkstra 假设弹出即最终最短，负权破坏它（LC 787 限制边数，用 Bellman-Ford 或带状态）（例：LC 787 K 站中转内最便宜的航班） |
| 有序数组，用哈希 | 双指针 | 有序是信号，哈希浪费空间（例：LC 167 两数之和 II；高频：LC 15 三数之和） |
| 第 `k` 大，排序 | 堆 / 快速选择 | 只要 `k` 个，不必全排；扫一遍只留前三名（例：LC 414 第三大的数；高频：LC 215 数组中的第 K 个最大元素） |
| 求「恰好 `k`」，直接做窗口 | 「至多 `k`」减「至多 `k-1`」 | 恰好不单调，至多单调（LC 1248、992）（例：LC 1248 统计「优美子数组」） |

- 判断是否换算法的标准：**这个性质是否单调**（窗口收缩 / 扩张、二分、双指针都依赖单调性），以及**局部选择是否影响后面**（贪心依赖无后效）。
- 用小反例检验：找一个 3 到 5 个元素的输入让自己的做法出错，找不出才继续写。

**例题：** LC 560 和为 K 的子数组

给整数数组 `nums` 和整数 `k`，统计并返回该数组中**和为 `k` 的子数组的个数**。子数组是数组中元素的连续非空序列。`1 <= nums.length <= 2 * 10^4`，`-1000 <= nums[i] <= 1000`，`-10^7 <= k <= 10^7`。

```python
from collections import Counter

def subarray_sum(nums: list[int], k: int) -> int:
    seen = Counter({0: 1})        # 前缀和 -> 出现次数；空前缀的和是 0
    pre = ans = 0
    for x in nums:
        pre += x
        ans += seen[pre - k]      # 以当前位置结尾、和为 k 的子数组个数
        seen[pre] += 1
    return ans
```

**例题：** LC 322 零钱兑换

给整数数组 `coins`（不同面额的硬币）和整数 `amount`（总金额），返回凑成总金额所需的**最少**硬币个数；凑不出来返回 `-1`。每种硬币的数量无限。`1 <= coins.length <= 12`，`1 <= coins[i] <= 2^31 - 1`，`0 <= amount <= 10^4`。

```python
def coin_change(coins: list[int], amount: int) -> int:
    inf = amount + 1                      # 哨兵：比任何真实答案都大
    dp = [0] + [inf] * amount             # dp[a] = 凑成金额 a 的最少硬币数
    for c in coins:                       # 完全背包：外层硬币，内层金额正序（同一枚硬币可重复用）
        for a in range(c, amount + 1):
            dp[a] = min(dp[a], dp[a - c] + 1)
    return dp[amount] if dp[amount] < inf else -1
```

**例题：** LC 3 无重复字符的最长子串

给字符串 `s`，求其中不含重复字符的**最长子串**的长度（子串必须连续）。`0 <= s.length <= 10^5`，字符是英文字母、数字、符号和空格。

```python
def length_of_longest_substring(s: str) -> int:
    last: dict[str, int] = {}          # 字符 -> 它最近一次出现的下标
    best = left = 0                    # 窗口是 s[left : right + 1]
    for right, ch in enumerate(s):
        if last.get(ch, -1) >= left:   # ch 在窗口内出现过：左端直接跳过去
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best
```

**例题：** LC 300 最长递增子序列

给整数数组 `nums`，求其中**最长严格递增子序列**的长度。子序列是删除（或不删除）若干元素、不改变其余元素相对顺序得到的序列，不要求连续。`1 <= nums.length <= 2500`，`-10^4 <= nums[i] <= 10^4`。进阶：能否做到 `O(n log n)`？

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

**例题：** LC 286 墙与门

给 `m × n` 的网格 `rooms`，格子的值是：`-1` 墙或障碍，`0` 一扇门，`INF = 2^31 - 1 = 2147483647` 一个空房间。原地给每个空房间填上它到**最近的门**的步数（上下左右移动，不能穿墙）；到不了任何门就保持 `INF`。`1 <= m, n <= 250`，值只会是 `-1`、`0`、`2^31 - 1`。

```python
from collections import deque

INF = 2**31 - 1

def walls_and_gates(rooms: list[list[int]]) -> None:
    m, n = len(rooms), len(rooms[0])
    queue = deque((r, c) for r in range(m) for c in range(n) if rooms[r][c] == 0)  # 所有门同时入队
    while queue:
        r, c = queue.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < m and 0 <= nc < n and rooms[nr][nc] == INF:   # 还没被填过的空房间
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

**例题：** LC 111 二叉树的最小深度

给二叉树的根 `root`，求它的最小深度：从根节点到**最近的叶子节点**的最短路径上的节点数。叶子节点是没有子节点的节点。树中节点数在 `[0, 10^5]` 内，`-1000 <= Node.val <= 1000`。

```python
from collections import deque
def min_depth(root: TreeNode | None) -> int:
    if root is None:
        return 0
    queue = deque([(root, 1)])                    # (节点, 它的深度)
    while queue:
        node, depth = queue.popleft()
        if node.left is None and node.right is None:
            return depth                          # BFS 按层推进：第一个叶子就是最浅的
        if node.left:
            queue.append((node.left, depth + 1))
        if node.right:
            queue.append((node.right, depth + 1))
    return 0
```

**例题：** LC 787 K 站中转内最便宜的航班

有 `n` 个城市通过一些航班连接。给数组 `flights`，`flights[i] = [from_i, to_i, price_i]` 表示从城市 `from_i` 到 `to_i` 的航班，价格 `price_i`。给定出发城市 `src`、目的地 `dst` 和整数 `k`，找出一条**最多经过 `k` 站中转**的路线，使从 `src` 到 `dst` 的价格最便宜，返回该价格；不存在则返回 `-1`。`2 <= n <= 100`，`0 <= flights.length <= n * (n - 1) / 2`，`0 <= from_i, to_i < n`，`from_i != to_i`，`1 <= price_i <= 10^4`，航班没有重复，没有自环，`0 <= src, dst, k < n`，`src != dst`。

```python
from math import inf


def find_cheapest_price(n: int, flights: list[list[int]], src: int, dst: int, k: int) -> int:
    # dp[t][v]：最多坐 t 趟航班，从 src 到城市 v 的最小价格
    dp: list[list[float]] = [[inf] * n for _ in range(k + 2)]
    dp[0][src] = 0                          # 0 趟航班：只在出发地，价格 0
    for t in range(1, k + 2):               # 最多 k 个中转 = 最多 k + 1 趟航班
        dp[t] = dp[t - 1][:]                # 少坐一趟也算（"最多 t 趟"）
        for u, v, w in flights:
            if dp[t - 1][u] + w < dp[t][v]:  # 只读上一行：这一行多坐的恰好一趟
                dp[t][v] = dp[t - 1][u] + w
    return -1 if dp[k + 1][dst] == inf else int(dp[k + 1][dst])
```

**例题：** LC 167 两数之和 II

给一个下标从 1 开始、按非递减顺序排列的整数数组 `numbers` 和目标值 `target`，找到唯一一对下标使两数之和等于 `target`，返回这两个下标；只能用常数级额外空间。`2 <= numbers.length <= 3 * 10^4`，`-1000 <= numbers[i] <= 1000`，`-1000 <= target <= 1000`。

```python
def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        total = numbers[left] + numbers[right]
        if total == target:
            return [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
    return []
```

**例题：** LC 414 第三大的数

给整数数组 `nums`，返回其中**第三大的数**；如果不存在，返回最大的数。「第三大」指在所有**不同**数字中排第三。`1 <= nums.length <= 10^4`，`-2^31 <= nums[i] <= 2^31 - 1`。进阶：`O(n)` 时间。

```python
def third_max(nums: list[int]) -> int:
    top: list[int] = []                        # 目前见过的最大的至多 3 个不同的值，降序
    for x in nums:
        if x in top:                           # 重复的数不占名次
            continue
        top.append(x)
        top.sort(reverse=True)                 # 最多 4 个元素，排序是 O(1)
        del top[3:]                            # 只留前 3 名
    return top[2] if len(top) == 3 else top[0]
```

**例题：** LC 1248 统计「优美子数组」

给整数数组 `nums` 和整数 `k`。如果某个连续子数组中**恰好**有 `k` 个奇数，就称它为「优美子数组」。返回数组中优美子数组的数目。`1 <= nums.length <= 50000`，`1 <= nums[i] <= 10^5`，`1 <= k <= nums.length`。

```python
def number_of_subarrays(nums: list[int], k: int) -> int:
    seen = [0] * (len(nums) + 1)            # seen[j]：前缀里“恰好有 j 个奇数”的位置有多少个
    seen[0] = 1                             # 空前缀
    odd = ans = 0
    for x in nums:
        odd += x & 1                        # 前缀里奇数个数
        if odd >= k:
            ans += seen[odd - k]            # 左边前缀的奇数个数为 odd - k，中间恰好 k 个奇数
        seen[odd] += 1
    return ans
```

**例题：** LC 127 单词接龙

字典 `wordList` 中从 `beginWord` 到 `endWord` 的**转换序列**是一个序列 `beginWord -> s1 -> s2 -> ... -> sk`：相邻两个单词只差一个字母；每个 `si`（`1 <= i <= k`）都在 `wordList` 中（`beginWord` 不需要在字典里）；`sk == endWord`。给 `beginWord`、`endWord` 和 `wordList`，返回从 `beginWord` 到 `endWord` 的**最短转换序列中的单词数目**；不存在则返回 `0`。约束：`1 <= beginWord.length <= 10`，`endWord.length == beginWord.length`，`1 <= wordList.length <= 5000`，`wordList[i].length == beginWord.length`，所有单词由小写英文字母组成，`beginWord != endWord`，`wordList` 中的字符串互不相同。

```python
import string
from collections import deque


def ladder_length(begin_word: str, end_word: str, word_list: list[str]) -> int:
    words = set(word_list)             # 还没访问过的词典单词；O(1) 查询
    if end_word not in words:
        return 0
    queue = deque([begin_word])
    steps = 1                          # 当前这一层的单词所在的序列长度
    while queue:
        for _ in range(len(queue)):    # 一次处理完整的一层
            word = queue.popleft()
            if word == end_word:
                return steps
            for i in range(len(word)):
                for ch in string.ascii_lowercase:
                    nxt = word[:i] + ch + word[i + 1:]
                    if nxt in words:
                        words.remove(nxt)          # 入队即标记已访问，防止重复入队
                        queue.append(nxt)
        steps += 1
    return 0
```

**例题：** LC 1091 二进制矩阵中的最短路径

给 `n x n` 的 0/1 矩阵 `grid`，求从左上角 `(0, 0)` 到右下角 `(n-1, n-1)` 的最短**畅通路径**的长度，不存在返回 `-1`。畅通路径要求经过的格子值都是 `0`，相邻格子在 **8 个方向**之一上连通（共边或共角）；路径长度是**经过的格子总数**。`n == grid.length == grid[i].length`，`1 <= n <= 100`，`grid[i][j]` 为 `0` 或 `1`。

```python
from collections import deque
from itertools import product

def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1                                    # 起点或终点被堵死
    dirs = [(dr, dc) for dr, dc in product((-1, 0, 1), repeat=2) if dr or dc]   # 8 个方向
    seen = [row[:] for row in grid]                  # 1 = 障碍或已入队；不改动入参
    seen[0][0] = 1
    q = deque([(0, 0, 1)])                           # (行, 列, 路径经过的格子数)
    while q:
        r, c, d = q.popleft()
        if r == n - 1 and c == n - 1:
            return d
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not seen[nr][nc]:
                seen[nr][nc] = 1                     # 入队时就标记，每格只入队一次
                q.append((nr, nc, d + 1))
    return -1
```

**例题：** LC 15 三数之和

给整数数组 `nums`，返回所有和为 `0` 且**不重复**的三元组 `[nums[i], nums[j], nums[k]]`，要求 `i`、`j`、`k` 互不相同；答案中不能包含重复的三元组，顺序不限。`3 <= nums.length <= 3000`，`-10^5 <= nums[i] <= 10^5`。

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)
    n = len(nums)
    result: list[list[int]] = []
    for i in range(n - 2):
        if nums[i] > 0:                            # 排好序后最小的数都 > 0，三数之和不可能为 0
            break
        if i > 0 and nums[i] == nums[i - 1]:       # 同一个"第一个数"只处理一次，去重
            continue
        lo, hi = i + 1, n - 1
        while lo < hi:
            total = nums[i] + nums[lo] + nums[hi]
            if total < 0:
                lo += 1
            elif total > 0:
                hi -= 1
            else:
                result.append([nums[i], nums[lo], nums[hi]])
                lo += 1
                hi -= 1
                while lo < hi and nums[lo] == nums[lo - 1]:   # 跳过重复的第二个数；第三个数随之唯一确定
                    lo += 1
    return result
```

**例题：** LC 215 数组中的第 K 个最大元素

给整数数组 `nums` 和整数 `k`，返回数组**排序后**的第 `k` 个最大元素（不是第 `k` 个不同的元素）。必须设计并实现时间复杂度为 `O(n)` 的算法。`1 <= k <= nums.length <= 10^5`，`-10^4 <= nums[i] <= 10^4`。

```python
import random

def find_kth_largest(nums: list[int], k: int) -> int:
    while True:
        pivot = random.choice(nums)
        bigger = [x for x in nums if x > pivot]
        equal = nums.count(pivot)
        if k <= len(bigger):                       # 答案在比 pivot 大的那一堆里
            nums = bigger
        elif k <= len(bigger) + equal:             # 落在 pivot 自己这一段
            return pivot
        else:                                      # 答案在比 pivot 小的那一堆里
            k -= len(bigger) + equal
            nums = [x for x in nums if x < pivot]
```
