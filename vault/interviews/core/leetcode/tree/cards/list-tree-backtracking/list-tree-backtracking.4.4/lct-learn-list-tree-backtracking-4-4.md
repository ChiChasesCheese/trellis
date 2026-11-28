---
id: lct-learn-list-tree-backtracking-4-4
node: list-tree-backtracking.4.4
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 回溯 › 排列型回溯**｜学习卡

套路是什么？

## A
**一句话。** 排列型回溯是「按位置填数」：第 `i` 位从没用过的元素里挑一个，用 `on_path` 标记已用；N 皇后、数独、分配问题是同一棵树，只在「没用过」之外加几条 `O(1)` 可查的冲突条件。

下图：按位置填数，第 `i` 层给第 `i` 位挑一个还没用过的数；`on_path` 记哪些已用。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 185">
<line x1="139.0" y1="26.9" x2="81.0" y2="63.1" stroke-width="1.2" stroke="currentColor"/>
<line x1="150.0" y1="33.0" x2="150.0" y2="57.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="161.0" y1="26.9" x2="219.0" y2="63.1" stroke-width="1.2" stroke="currentColor"/>
<line x1="63.1" y1="81.0" x2="46.9" y2="107.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="76.9" y1="81.0" x2="93.1" y2="107.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="40.0" y1="131.0" x2="40.0" y2="149.0" stroke-width="1.2" stroke="currentColor"/>
<line x1="100.0" y1="131.0" x2="100.0" y2="149.0" stroke-width="1.2" stroke="currentColor"/>
<circle cx="150" cy="20" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150" y="24" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor"></text>
<circle cx="70" cy="70" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="70" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="150" cy="70" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="230" cy="70" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="74" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="40" cy="118" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="40" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="100" cy="118" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="40" cy="162" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="40" y="166" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<circle cx="100" cy="162" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="100" y="166" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">2</text>
<text x="150" y="100" text-anchor="middle" font-size="14" font-family="sans-serif" style="fill:var(--dim,#6b7280)">…</text>
<text x="230" y="100" text-anchor="middle" font-size="14" font-family="sans-serif" style="fill:var(--dim,#6b7280)">…</text>
<text x="140" y="140" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">path = [1, 2, 3]</text>
<rect x="140" y="152" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="153.0" y="167.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">T</text>
<rect x="166" y="152" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="179.0" y="167.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">T</text>
<rect x="192" y="152" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="205.0" y="167.0" text-anchor="middle" font-size="10" font-family="sans-serif" fill="currentColor">T</text>
<text x="230" y="168" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">on_path</text>
<text x="8" y="18" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">每层从 0 扫起</text>
<text x="8" y="34" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">跳过已用的</text>
<text x="240" y="18" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第 i 层 = 第 i 位</text>
</svg>

```python
def permute(nums):                   # LC 46
    n = len(nums)
    ans, path = [], [0] * n          # path[i]：第 i 位填什么
    on_path = [False] * n            # nums[j] 是否已被用
    def dfs(i):
        if i == n:
            ans.append(path[:])      # 拷贝
            return
        for j in range(n):           # 每层从 0 扫起：顺序有区别
            if not on_path[j]:
                path[i] = nums[j]    # 覆盖，不用 pop
                on_path[j] = True
                dfs(i + 1)
                on_path[j] = False   # 恢复现场
    dfs(0)
    return ans
```

**要点。**
- 为什么对？：第 `i` 层有 `n - i` 个孩子，叶子 `n!` 个，不同叶子的前缀必在某一位不同，不重不漏；`on_path` 恒等于 `path[:i]` 的元素集合，进入置位、退出复位。
- LC 51、LC 52 怎么改？：行当层数，列的排列加两条对角线标记：列 `c`、副对角线 `r + c`、主对角线 `r - c + n - 1`（加 `n - 1` 防负下标），三个标记一起置位、一起复位；51 叶子处画棋盘，52 只计数，可用位掩码。
- LC 2850 怎么改？：先化简成「多余石头（一格 `k` 颗算 `k - 1` 颗）与空格一一配对」，空格的排列就是配对方案，叶子处取累计曼哈顿距离的最小值。
- LC 37 怎么改？：位置换成所有空格，候选来自行、列、宫三个位掩码的补集，成功立刻向上返回 `True` 不再回溯。

**易错点。**
- 把组合型「往后选」带进来：`[1,2,3]` 只得 `[[1,2,3]]`，应有 `6` 个。
- `ans.append(path)` 不拷贝：覆盖式 `path` 最后是 `[3,2,1]`，得到 `6` 个 `[3,2,1]`。
- N 皇后只查列和一个方向的对角线：`n = 4` 应有 `2` 个解；复位漏掉对角线标记会只剩 `0` 个。

**对应题目。** LC 2850 将石头分散到网格图的最少移动次数、LC 52 N 皇后 II、LC 51 N 皇后、LC 46 全排列、LC 37 解数独（Sudoku Solver）
