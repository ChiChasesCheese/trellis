---
id: uth-devtools-git-objects-2-merkle
node: devtools.git-objects
type: qa
step: 2
---
## Q
**提交为什么是 DAG**｜Git · 对象模型

改一个文件，哪些对象的哈希会跟着变？分支又是什么？

## A
**背景。** 一次提交要记录两件事：此刻整个目录的样子，以及它从哪个提交演变而来。git 用对象串起来：commit（提交）指向一个 tree（目录对象），再指向父提交。每个对象的名字是它内容的哈希，而内容里又含着子对象的哈希，所以改动任何一处，沿路向上的哈希都会跟着变。

**结构。** tree 记录每个条目的（模式、名字、子对象哈希）；commit 记录根 tree 的哈希、父提交的哈希（可以有多个）、作者和说明。整段历史是默克尔（Merkle）有向无环图：用哈希把节点连起来的 DAG。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<circle cx="40" cy="70" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="40" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">A</text>
<circle cx="110" cy="70" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">B</text>
<circle cx="180" cy="70" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="180" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">C</text>
<circle cx="110" cy="130" r="13" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="134" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">D</text>
<circle cx="262" cy="100" r="13" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="262" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">M</text>
<line x1="97" y1="70" x2="58" y2="70" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M53.0,70.0 L59.8,66.7 L59.8,73.3 Z" fill="currentColor" stroke="none"/>
<line x1="167" y1="70" x2="128" y2="70" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M123.0,70.0 L129.8,66.7 L129.8,73.3 Z" fill="currentColor" stroke="none"/>
<line x1="100" y1="121" x2="52.8597" y2="82.1785" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M49.0,79.0 L56.3,80.8 L52.1,85.8 Z" fill="currentColor" stroke="none"/>
<line x1="250" y1="94" x2="197.743" y2="76.5811" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M193.0,75.0 L200.4,74.0 L198.4,80.2 Z" fill="currentColor" stroke="none"/>
<line x1="249" y1="105" x2="127.919" y2="127.102" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M123.0,128.0 L129.1,123.6 L130.2,130.0 Z" fill="currentColor" stroke="none"/>
<rect x="232" y="20" width="60" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="262" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">main</text>
<line x1="262" y1="44" x2="262" y2="80" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M262.0,85.0 L258.7,78.2 L265.3,78.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="80" y="170" width="60" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="110" y="186" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">feature</text>
<line x1="110" y1="170" x2="110" y2="150" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M110.0,145.0 L113.3,151.8 L106.7,151.8 Z" fill="currentColor" stroke="none"/>
<text x="250" y="176" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">合并提交 M</text>
<text x="250" y="192" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">有两个父</text>
</svg>
```

**细节。**

- 改一个文件：新 blob，到它所有上层目录的新 tree，再到新 commit，其余子树原样复用
- 合并提交有两个父，所以历史是 DAG 而不是链
- 分支只是 `.git/refs/heads/<名字>` 里的一个 40 字符提交哈希，建分支就是写一个文件

**为什么。** 父对象的哈希包含了子对象的哈希，根哈希就能证明整棵树和整段历史没被改过；比较两棵树时，哈希相同的子树直接跳过。

**例题：** LC 236 二叉树的最近公共祖先

给一棵二叉树和其中两个节点 `p`、`q`，找出它们的最近公共祖先（一个节点也可以是它自己的祖先），节点值互不相同。例：`root=[3,5,1,6,2,0,8,null,null,7,4]`，`p=5, q=1` → 3；`p=5, q=4` → 5。

```python
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    parent: dict[TreeNode, TreeNode | None] = {root: None}
    stack = [root]
    while p not in parent or q not in parent:      # p、q 的父指针都登记好就停
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                parent[child] = node
                stack.append(child)
    ancestors: set[TreeNode] = set()
    node: TreeNode | None = p
    while node:                                    # p 自己和它的全部祖先
        ancestors.add(node)
        node = parent[node]
    node = q
    while node not in ancestors:                   # q 往上爬，第一个撞上的就是答案
        node = parent[node]
    return node
```
