---
id: tlc-scramble-string-0-whole
node: b.scramble-string
type: qa
---
## Q
**LC 87 扰乱字符串**｜Hard · CodeTop 国内累计 2 次 · 最近 2026-05-29（CodeTop）

扰乱算法：长度为 1 时停止；长度大于 1 时，在某个位置把字符串切成两个非空子串 `x`、`y`（`s = x + y`），随机决定保持 `x + y` 或交换成 `y + x`，再对 `x`、`y` 分别递归执行。给两个长度相等的字符串 `s1`、`s2`，判断 `s2` 能否由 `s1` 扰乱得到。`s1.length == s2.length`，`1 <= s1.length <= 30`，只含小写字母。 例：`s1 = "great", s2 = "rgeat"` → `true`（`"gr|eat"` 不交换，再把 `"g|r"` 交换成 `"rg"`，其余不变）；`s1 = "abcde", s2 = "caebd"` → `false`；`s1 = "a", s2 = "a"` → `true`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 区间 DP（记忆化搜索）：`dfs(i, j, L)` 表示 `s1[i:i+L]` 能否扰乱成 `s2[j:j+L]`；枚举第一刀的位置 `k`，不交换时左段对左段、右段对右段，交换时 `s1` 的前 `k` 个对 `s2` 的后 `k` 个；字符计数不同直接剪掉。状态 `O(n^3)`，每个 `O(n)`，共 `O(n^4)`。

**识别。** 「递归地切成两段、每段可以交换」→ 扰乱过程是一棵二叉树，子问题是「两段等长子串能否互相扰乱」，由两个起点 `i`、`j` 和长度 `L` 决定 → 三维区间 DP。`n <= 30` → `n^4 ≈ 8 * 10^5`，可行；不记忆的递归是指数级。

**推导。** 暴力：生成 `s1` 的全部扰乱结果再查 `s2` 在不在里面，结果数随长度指数增长。改成判定：`s1` 的第一刀把它切成长度 `k` 和 `L - k` 的两段。若这一层不交换，`s2` 的前 `k` 个必须是 `s1` 前段的扰乱、后段同理；若交换，`s2` 的后 `k` 个对应 `s1` 的前段。每次判定拆成两个更短的同类子问题，而子问题只由 `(i, j, L)` 决定，最多 `n^3` 个，用 `@cache` 记下来。两段字符多重集不同时一定不行，提前返回，剪掉大部分分支。

```python
from collections import Counter
from functools import cache


def is_scramble(s1: str, s2: str) -> bool:
    @cache
    def dfs(i: int, j: int, length: int) -> bool:
        # s1[i : i+length] 能否扰乱成 s2[j : j+length]
        a, b = s1[i:i + length], s2[j:j + length]
        if a == b:
            return True
        if Counter(a) != Counter(b):                      # 字符多重集不同，一定不行（剪枝）
            return False
        for k in range(1, length):                        # s1 这段在第 k 个字符后切开
            # 不交换：前 k 个对 s2 的前 k 个，后段对后段
            if dfs(i, j, k) and dfs(i + k, j + k, length - k):
                return True
            # 交换：s1 的前 k 个对 s2 的后 k 个，s1 的后段对 s2 的前段
            if dfs(i, j + length - k, k) and dfs(i + k, j, length - k):
                return True
        return False

    return dfs(0, 0, len(s1))
```

运行：`"great", "rgeat"` → `True`，`"abcde", "caebd"` → `False`，`"a", "a"` → `True`，`"abc", "bca"` → `True`，`"abcd", "bdac"` → `False`。

**复杂度。** 状态 `O(n^3)`，每个状态枚举 `k` 是 `O(n)`，切片和 `Counter` 也是 `O(n)`，总时间 `O(n^4)`；空间 `O(n^3)` 的缓存，递归深度 `O(n)`。

**易错点。**
- 交换分支的下标：`s1` 的前 `k` 个要对 `s2` 的**后** `k` 个，即 `dfs(i, j + length - k, k)`。误写成 `dfs(i, j + k, k)` 时 `"abc", "bca"` 得到 `False`（正确 `True`：`"a|bc"` 交换成 `"bc" + "a"`）。
- 只比较字符计数：计数相同是必要条件不是充分条件，`"abcde", "caebd"` 计数相同，答案却是 `False`。
- 忘了 `@cache`：同一个 `(i, j, L)` 被反复求解，退化成指数级。

**追问。**
- 自底向上：`dp[L][i][j]` 三维表，按长度从小到大填，没有递归。
- 输出一种扰乱方式：`dfs` 返回 `True` 时记下 `(k, 是否交换)`，再递归重建出二叉树。
- 计数剪枝更快：预先算 26 维前缀计数，比较两段的字符多重集从 `O(L)` 降到 `O(26)`。

**同模式。** LC 312 戳气球、LC 1039 多边形三角剖分的最低得分、LC 241 为运算表达式设计优先级、LC 95 不同的二叉搜索树 II。
