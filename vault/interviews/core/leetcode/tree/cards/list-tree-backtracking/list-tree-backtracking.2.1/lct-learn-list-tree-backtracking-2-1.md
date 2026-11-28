---
id: lct-learn-list-tree-backtracking-2-1
node: list-tree-backtracking.2.1
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 遍历二叉树**｜学习卡

套路是什么？

## A
**一句话。** 递归遍历二叉树，三种顺序只差「访问当前节点」写在两次递归的前、中、后哪一处：前序是根左右，中序是左根右，后序是左右根。

下图：每个节点被经过三次，三种顺序只差在哪一次记录。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 175">
<line x1="81.9" y1="40.2" x2="58.1" y2="69.8" stroke-width="1.2" stroke="currentColor"/>
<line x1="98.1" y1="40.2" x2="121.9" y2="69.8" stroke-width="1.2" stroke="currentColor"/>
<line x1="44.2" y1="91.6" x2="30.8" y2="118.4" stroke-width="1.2" stroke="currentColor"/>
<line x1="55.8" y1="91.6" x2="69.2" y2="118.4" stroke-width="1.2" stroke="currentColor"/>
<circle cx="90" cy="30" r="13" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="90" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<circle cx="50" cy="80" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="50" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<circle cx="130" cy="80" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="130" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<circle cx="25" cy="130" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="25" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<circle cx="75" cy="130" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="62" y="22" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">①</text>
<text x="90" y="58" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">②</text>
<text x="118" y="22" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③</text>
<text x="175" y="34" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">① 前序：进门就记</text>
<text x="175" y="52" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">② 中序：左子树回来后</text>
<text x="175" y="70" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">③ 后序：出门才记</text>
<text x="175" y="104" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">前序 1 2 4 5 3</text>
<text x="175" y="122" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">中序 4 2 5 1 3</text>
<text x="175" y="140" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">后序 4 5 2 3 1</text>
<text x="170" y="168" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同一个 dfs，只差记录写在哪一行</text>
</svg>

```python
def traverse(root):
    pre, ino, post = [], [], []

    def dfs(node):
        if node is None:             # 空节点是递归边界
            return
        pre.append(node.val)         # 前序：进门就记
        dfs(node.left)
        ino.append(node.val)         # 中序：左子树之后
        dfs(node.right)
        post.append(node.val)        # 后序：出门才记

    dfs(root)
    return pre, ino, post
```

**要点。**
- 为什么对？：每个节点恰好被访问一次，记录的时机决定顺序；`O(n)` 时间，栈深是树高。
- LC 94 怎么改？：只保留中序那一行；二叉搜索树的中序序列是升序。
- 迭代怎么改？：用显式栈模拟递归：一路向左入栈，弹出时记录，再转向右子树。

**易错点。**
- 记录位置写错：中序写在 `dfs(node.left)` 之前就成了前序。
- 链状的树（`[1,null,2,null,3]`）：递归深度等于节点数，极端数据会栈溢出，必要时改迭代。

**对应题目。** LC 94 二叉树的中序遍历
