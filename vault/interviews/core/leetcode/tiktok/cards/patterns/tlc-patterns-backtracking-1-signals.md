---
id: tlc-patterns-backtracking-1-signals
node: patterns.backtracking
type: qa
step: 1
---
## Q
**回溯（Backtracking）｜信号**

什么样的题面该想到回溯？数据范围怎样帮你确认？哪些近似信号其实要 DP 或贪心？

## A
回溯（Backtracking）= 深度优先地**枚举所有候选**，每一步做一个选择，递归下去，回来后**撤销选择**再试下一个。它的搜索树是指数级的，靠**剪枝**砍掉不可能的分支。

**触发信号：**
- 要求**列出所有**方案：子集 LC 78、组合 LC 39 / 77、排列 LC 46、括号生成 LC 22、复原 IP LC 93（例：LC 78 子集）。
- 在棋盘 / 网格里**找一条路径或一种摆放**：N 皇后 LC 51、单词搜索 LC 79（例：LC 79 单词搜索）。
- 数据范围很小：`n <= 8` 到 `n <= 20`（LC 51 的 `n <= 9`，LC 473 的 `matchsticks.length <= 15`，LC 78 的 `nums.length <= 10`，LC 22 的 `n <= 8`）。指数级复杂度只有在这种范围才可行（例：LC 784 字母大小写全排列）。
- 约束要**边选边检查**：括号必须匹配、皇后不能互攻、和不能超过目标（例：LC 39 组合总和）。

**近似信号：**
- 只问**方案个数**或**最优值**，且有重叠子问题 ⇒ DP（LC 322、139、62），回溯会超时（例：LC 62 不同路径）。
- 每步局部最优就能得到全局最优 ⇒ 贪心（例：LC 55 跳跃游戏）。
- 数据范围到 `10^5` ⇒ 绝不是回溯（例：LC 3 无重复字符的最长子串）。
- 只要判断"存在"一种可行方案，且分支多 ⇒ 回溯加剪枝，或 DP / 位掩码（例：LC 416 分割等和子集）。
- 排列 / 组合的个数本身就是指数级：输出规模决定了复杂度下限，不用试图优化到多项式（例：LC 90 子集 II）。

**例题：** LC 78 子集

给定元素互不相同的整数数组 `nums`（`1 <= nums.length <= 10`），返回它所有可能的子集（幂集），不含重复子集，顺序不限。

```python
def subsets(nums: list[int]) -> list[list[int]]:
    res: list[list[int]] = []
    path: list[int] = []
    def dfs(start: int) -> None:
        res.append(path[:])                 # 每个节点都是一个子集：进来先记一份快照
        for i in range(start, len(nums)):   # 只往后选，保证同一个子集不会按不同顺序出现两次
            path.append(nums[i])
            dfs(i + 1)
            path.pop()                      # 回溯：撤销选择
    dfs(0)
    return res
```

**例题：** LC 79 单词搜索

给定 `m x n` 字符网格 `board` 和字符串 `word`，判断 `word` 能否由网格里水平或垂直相邻的单元格按顺序拼出，同一单元格不可重复使用。`1 <= m, n <= 6`，`1 <= word.length <= 15`。

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    def backtrack(r: int, c: int, i: int) -> bool:
        if i == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
            return False
        temp, board[r][c] = board[r][c], "#"  # 临时占位，防止本条路径重复使用
        found = any(backtrack(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = temp
        return found
    return any(backtrack(r, c, 0) for r in range(rows) for c in range(cols))
```

**例题：** LC 784 字母大小写全排列

给定字符串 `s`（`1 <= s.length <= 12`，由字母和数字组成），把其中每个字母独立地转成大写或小写，返回所有可能得到的字符串，顺序不限。

```python
def letter_case_permutation(s: str) -> list[str]:
    res: list[str] = []
    path = list(s)                      # 原地改字符，回溯时改回来
    def dfs(i: int) -> None:
        if i == len(path):
            res.append("".join(path))
            return
        dfs(i + 1)                      # 这一位保持原样
        if path[i].isalpha():           # 只有字母才有第二个分支
            path[i] = path[i].swapcase()
            dfs(i + 1)
            path[i] = path[i].swapcase()   # 回溯：还原
    dfs(0)
    return res
```

**例题：** LC 39 组合总和

给定无重复元素的整数数组 `candidates`（`1 <= candidates.length <= 30`，`2 <= candidates[i] <= 40`）和目标 `target`（`1 <= target <= 40`），找出所有和为 `target` 的不同组合，每个数可无限次重复选取。

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates = sorted(candidates)
    out: list[list[int]] = []
    path: list[int] = []
    def go(start: int, remain: int) -> None:
        if remain == 0:
            out.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break                        # 已排序：后面的数只会更大
            path.append(candidates[i])
            go(i, remain - candidates[i])    # 传 i 而不是 i + 1：同一个数可以重复选
            path.pop()
    go(0, target)
    return out
```

**例题：** LC 62 不同路径

机器人在 `m x n` 网格左上角，每次只能向下或向右走一步，求走到右下角的不同路径数。`1 <= m, n <= 100`，答案不超过 `2 * 10^9`。

```python
def unique_paths(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]                 # 第一行、第一列都只有 1 条路
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]   # 最后一步从上来，或从左来
    return dp[m - 1][n - 1]
```

**例题：** LC 55 跳跃游戏

非负整数数组 `nums`（`1 <= nums.length <= 10^4`），`nums[i]` 是在下标 `i` 能跳的最大长度，从下标 0 出发，判断能否到达最后一个下标。

```python
def can_jump(nums: list[int]) -> bool:
    reach = 0                               # 目前能到达的最远下标
    for i, step in enumerate(nums):
        if i > reach:
            return False                    # 连 i 都够不着，后面更不可能
        reach = max(reach, i + step)
    return True
```

**例题：** LC 3 无重复字符的最长子串

给定字符串 `s`（`0 <= s.length <= 10^5`），求不含重复字符的最长子串的长度。

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

**例题：** LC 416 分割等和子集

只含正整数的非空数组 `nums`（`1 <= nums.length <= 200`，`1 <= nums[i] <= 100`），判断能否分成两个元素和相等的子集。

```python
def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2:
        return False                           # 总和是奇数，不可能平分
    n, half = len(nums), total // 2
    dp = [[False] * (half + 1) for _ in range(n + 1)]
    dp[0][0] = True                            # 基础行：一个数都不选，只能凑出 0
    for i in range(1, n + 1):
        x = nums[i - 1]
        for j in range(half + 1):
            dp[i][j] = dp[i - 1][j] or (j >= x and dp[i - 1][j - x])   # 不选第 i 个 / 选第 i 个
    return dp[n][half]                         # 答案格：用全部 n 个数，凑出 half
```

**例题：** LC 90 子集 II

整数数组 `nums` 可能含重复元素（`1 <= nums.length <= 10`，`-10 <= nums[i] <= 10`），返回所有不重复的子集，顺序不限。

```python
def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums = sorted(nums)                         # 排序让相同的数相邻，才能“同层跳过”
    path: list[int] = []
    res: list[list[int]] = []
    def backtrack(start: int) -> None:
        res.append(path[:])                     # 每个节点本身就是一个子集
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:   # 同一层里相同的数只选第一个，避免生成重复子集
                continue
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()
    backtrack(0)
    return res
```
