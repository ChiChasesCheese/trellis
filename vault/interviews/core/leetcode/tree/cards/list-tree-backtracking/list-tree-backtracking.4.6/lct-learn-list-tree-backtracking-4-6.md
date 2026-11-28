---
id: lct-learn-list-tree-backtracking-4-6
node: list-tree-backtracking.4.6
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 回溯 › 搜索**｜学习卡

套路是什么？

## A
**一句话。** 搜索题没有现成骨架，先答三件事：状态是什么、一步有哪些合法走法、何时提前放弃；然后统一「改状态 → 递归 → 还原状态」DFS 整个状态空间，剪枝决定它能不能在数据范围内跑完。

下图：LC 79 的 DFS 骨架：先剪枝，再「改状态 → 递归 → 还原状态」。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260">
<rect x="35.8" y="7.5" width="228.4" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">状态：站在 (i, j)，要匹配 word[k]</text>
<polygon points="89.2,66.0 98.2,53.5 201.8,53.5 210.8,66.0 201.8,78.5 98.2,78.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="70.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">这格 ≠ word[k]？</text>
<rect x="267.0" y="53.5" width="56" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="295" y="70.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">False</text>
<polygon points="93.0,112.0 102.0,99.5 198.0,99.5 207.0,112.0 198.0,124.5 102.0,124.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="116.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k 已是最后一位？</text>
<rect x="267.0" y="99.5" width="56" height="25" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="295" y="116.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">True</text>
<rect x="87.0" y="145.5" width="125.9" height="25" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150" y="162.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改状态：这格标成 #</text>
<rect x="76.0" y="187.5" width="148" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="150" y="204.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">四个方向递归，成功就停</text>
<rect x="88.0" y="229.5" width="124" height="25" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="150" y="246.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">还原这格，返回结果</text>
<path d="M 150.0 32.5 L 150.0 53.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,53.5 147.0,47.2 153.0,47.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 210.8 66.0 L 267.0 66.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="267.0,66.0 260.7,69.0 260.7,63.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="232" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 150.0 78.5 L 150.0 99.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,99.5 147.0,93.2 153.0,93.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="158.0" y="93.0" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 207.0 112.0 L 267.0 112.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="267.0,112.0 260.7,115.0 260.7,109.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="232" y="106" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">是</text>
<path d="M 150.0 124.5 L 150.0 145.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,145.5 147.0,139.2 153.0,139.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="158.0" y="139.0" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<path d="M 150.0 170.5 L 150.0 187.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,187.5 147.0,181.2 153.0,181.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 150.0 212.5 L 150.0 229.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,229.5 147.0,223.2 153.0,223.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>

```python
def exist(board, word):              # LC 79
    m, n = len(board), len(board[0])
    def dfs(i, j, k):                # 站在 (i, j)，要匹配 word[k]
        if board[i][j] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        ch, board[i][j] = board[i][j], '#'   # 标记本路径已用
        found = False
        for x, y in (i+1, j), (i-1, j), (i, j+1), (i, j-1):
            if 0 <= x < m and 0 <= y < n and dfs(x, y, k+1):
                found = True
                break                # 存在型：成功就不再试别的
        board[i][j] = ch             # 还原：别的路径还能用这格
        return found
    return any(dfs(i, j, 0)
               for i in range(m) for j in range(n))
```

**要点。**
- 为什么对？：搜索树结点是状态、边是合法走法，DFS 遍历整棵树不会漏；还原保证兄弟分支看到同一个起点。格子可在不同路径里重复访问，所以与数岛屿不同，必须还原标记。
- LC 473、LC 282 怎么改？：473 状态是四条边当前长度，火柴从长到短放，总长不能被 `4` 整除或有火柴比边长还长直接失败，当前长度相同的边只试第一条；282 枚举下一项取几位、前接 `+ - *`，状态带最后一项 `last`，乘法用 `total - last + last * x`，数字有前导零就 `break`。
- LC 679、LC 126 怎么改？：679 每步从剩下的数里选有序的两个做四则运算合并，只剩一个数且为 `24` 时成功，用 `Fraction` 防浮点误差；126 先 BFS 按层记每个词的所有父亲（整层处理完才登记 `seen`），再从终点沿父亲回溯展开所有最短路径。
- LC 17 怎么做？：每位从候选字母里选一个，没有剪枝，是最简单的搜索。

**易错点。**
- 忘了还原 `#`：`[["b","a","a"]]`、`"aab"` 应得 `True`，不还原会得 `False`。
- LC 282 乘法写成 `total * x`：`"232"`、`target = 8` 应得 `["2*3+2","2+3*2"]`；允许前导零：`"105"`、`target = 5` 应得 `["1*0+5","10-5"]`。
- LC 679 用 `float` 比较 `== 24`：`[3,3,8,8]` 应得 `True`，`8 / (3 - 8/3)` 在浮点里是 `23.999…`。

**对应题目。** LC 679 24 点游戏、LC 282 给表达式添加运算符、LC 17 电话号码的字母组合、LC 473 火柴拼正方形、LC 126 单词接龙 II、LC 79 单词搜索
