---
id: lct-learn-list-tree-backtracking-2-12
node: list-tree-backtracking.2.12
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 树形 DP**｜学习卡

套路是什么？

## A
**一句话。** 树形 DP 是自底向上 DFS 返回一组状态值：状态编码「父亲需要知道的一切」（选没选、有没有摄像头、是否被覆盖），固定了节点自己的状态后左右子树互不干扰，只在父亲处合并。

下图：LC 337，每个节点向上返回一组状态，父亲只用孩子的状态合并；答案 `max(7, 6) = 7`。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<line x1="101.3" y1="34.6" x2="68.7" y2="70.4" stroke-width="1.2" stroke="currentColor"/>
<line x1="118.7" y1="34.6" x2="151.3" y2="70.4" stroke-width="1.2" stroke="currentColor"/>
<line x1="65.4" y1="91.8" x2="79.6" y2="123.2" stroke-width="1.2" stroke="currentColor"/>
<line x1="165.4" y1="91.8" x2="179.6" y2="123.2" stroke-width="1.2" stroke="currentColor"/>
<circle cx="110" cy="25" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="110" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<circle cx="60" cy="80" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="160" cy="80" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="85" cy="135" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="85" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="185" cy="135" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="185" y="139" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="110" y="6" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)"></text>
<text x="150" y="22" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">(7, 6)</text>
<text x="14" y="84" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">(2, 3)</text>
<text x="178" y="84" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">(3, 1)</text>
<text x="85" y="164" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">(3, 0)</text>
<text x="185" y="164" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">(1, 0)</text>
<text x="225" y="50" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每个节点返回</text>
<text x="225" y="66" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">(偷, 不偷)</text>
<text x="225" y="96" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">偷 = val + 左不偷</text>
<text x="245" y="112" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">+ 右不偷</text>
<text x="225" y="132" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">不偷 = max(左)</text>
<text x="245" y="148" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">+ max(右)</text>
</svg>

```python
def rob(root):                       # LC 337，两个状态
    def dfs(node):                   # 返回 (偷, 不偷)
        if not node:
            return 0, 0
        lr, ln = dfs(node.left)
        rr, rn = dfs(node.right)
        return node.val + ln + rn, max(lr, ln) + max(rr, rn)
    return max(dfs(root))

def min_camera_cover(root):          # LC 968，三个状态
    def dfs(node):                   # (装, 靠父亲, 靠孩子)
        if not node:
            return inf, 0, 0         # 空节点不能装，也无需被覆盖
        lc, lf, lb = dfs(node.left)
        rc, rf, rb = dfs(node.right)
        return (min(lc, lf, lb) + min(rc, rf, rb) + 1,  # 装
                min(lc, lb) + min(rc, rb),  # 靠父亲
                min(lc + rc, lc + rb, lb + rc))  # 靠孩子
    c, _, b = dfs(root)
    return min(c, b)                 # 根没有父亲：不能靠父亲
```

**要点。**
- 为什么对？：约束只发生在父子之间，固定节点自己的状态后，左右子树各取与该状态相容的最优再相加；每个子问题只依赖子树本身。
- 状态怎么选？：父亲只通过状态了解孩子，状态要不重不漏。337 看孩子偷没偷；968 看孩子自己装了、靠父亲、靠孩子三类。
- 不可能的状态怎么表示？：用 `inf`，叶子的「靠孩子覆盖」自然排除。

**易错点。**
- LC 337 不偷时写成 `ln + rn`：`[3,4,5,1,3,null,1]` 应得 `9`，写错只得 `3`；孩子可偷可不偷，要取 `max`。
- LC 968 空节点返回 `(0, 0, 0)`：`[0]` 应得 `1`，写错得 `0`；根取三个状态的最小值也得 `0`，要排除靠父亲。
- LC 968 靠孩子覆盖只写 `lc + rc`：`[0,0,null,0,0]` 应得 `1`，漏掉一装一被覆盖的组合会得 `2`。

**对应题目。** LC 968 监控二叉树、LC 337 打家劫舍 III
