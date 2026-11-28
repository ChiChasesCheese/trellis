---
id: lct-learn-list-tree-backtracking-2-8
node: list-tree-backtracking.2.8
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 最近公共祖先**｜学习卡

套路是什么？

## A
**一句话。** 后序 DFS 让每棵子树汇报「我这里找到了谁」：碰到目标就返回自己，左右都汇报非空说明目标分居两侧，当前节点就是最近公共祖先（LCA），否则把非空的一侧原样上传。

下图：后序汇报；p、q 分居两侧时，第一个左右都非空的节点就是 LCA。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<line x1="110.4" y1="33.7" x2="74.6" y2="66.3" stroke-width="1.2" stroke="currentColor"/>
<line x1="129.6" y1="33.7" x2="165.4" y2="66.3" stroke-width="1.2" stroke="currentColor"/>
<line x1="58.3" y1="86.1" x2="41.7" y2="113.9" stroke-width="1.2" stroke="currentColor"/>
<line x1="71.7" y1="86.1" x2="88.3" y2="113.9" stroke-width="1.2" stroke="currentColor"/>
<line x1="168.3" y1="86.1" x2="151.7" y2="113.9" stroke-width="1.2" stroke="currentColor"/>
<line x1="181.7" y1="86.1" x2="198.3" y2="113.9" stroke-width="1.2" stroke="currentColor"/>
<circle cx="120" cy="25" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="120" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3</text>
<circle cx="65" cy="75" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="65" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<circle cx="175" cy="75" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="175" y="79" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="35" cy="125" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="35" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<circle cx="95" cy="125" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="145" cy="125" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<circle cx="205" cy="125" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="205" y="129" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<text x="35" y="152" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">p</text>
<text x="205" y="152" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">q</text>
<text x="95" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">None</text>
<text x="145" y="152" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">None</text>
<text x="70" y="48" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑p</text>
<text x="170" y="48" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">↑q</text>
<text x="240" y="30" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">左右都非空：</text>
<text x="240" y="46" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">3 就是 LCA</text>
<text x="240" y="90" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">只一侧非空：</text>
<text x="240" y="106" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">原样上传</text>
<text x="170" y="172" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每棵子树汇报「我这里找到了谁」</text>
</svg>

```python
def lca(root, p, q):                 # LC 236
    if root is None or root is p or root is q:
        return root                  # 找到目标（或走到底）就上报
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:               # 目标分居两侧：这里是分叉点
        return root
    return left or right             # 都在一侧或都没有：原样上传

def lca_deepest(root):               # LC 1123
    def dfs(node):                   # 返回 (最深叶深度, 它们的 LCA)
        if node is None:
            return 0, None
        ld, ln = dfs(node.left)
        rd, rn = dfs(node.right)
        if ld != rd:
            return (ld + 1, ln) if ld > rd else (rd + 1, rn)
        return ld + 1, node          # 一样深：最深叶子分居两侧
    return dfs(root)[1]
```

**要点。**
- 为什么对？：`f(node)` 在子树含两个目标时是它们的 LCA，含一个时是那一个，含零个是 `None`；`node` 自己是目标时不用再往下搜，另一个目标若在其下，它就是 LCA，否则由祖先在另一侧汇合。
- LC 235、LC 1676 怎么改？：235 利用 BST，都小往左、都大往右，否则当前节点就是答案；1676 把 `root is p or root is q` 换成 `root in targets`。
- LC 1650 怎么改？：节点带父指针，两个指针各自向上走，走到顶就换到对方起点，和链表求相交同构。
- LC 1740、LC 2096 怎么改？：先找 LCA，两点路径拆成两段；1740 距离是两段边数之和，2096 求根到两点的 `L/R` 串，去掉共同前缀，起点剩下的全换成 `U` 再接终点剩下的。

**易错点。**
- 一个目标是另一个的祖先：`[3,5,1,6,2,0,8,null,null,7,4]`、`p = 5`、`q = 4` 应得 `5`。
- LC 1123 深度相等时没返回当前节点：`[3,5,1]` 应得 `3`，不是 `5`。
- LC 2096 忘了去共同前缀：`[5,1,2,3,null,6,4]` 起点 `3`、终点 `1`，应得 `"U"`，不去前缀会得 `"UUL"`。

**对应题目。** LC 1740 找到二叉树中的距离、LC 235 二叉搜索树的最近公共祖先、LC 1650 二叉树的最近公共祖先 III、LC 1676 二叉树的最近公共祖先 IV、LC 236 二叉树的最近公共祖先、LC 1123 最深叶节点的最近公共祖先、LC 2096 从二叉树一个节点到另一个节点每一步的方向
