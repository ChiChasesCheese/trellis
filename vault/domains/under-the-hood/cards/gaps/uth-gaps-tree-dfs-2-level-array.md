---
id: uth-gaps-tree-dfs-2-level-array
node: gaps.tree-dfs
type: qa
step: 2
---
## Q
**du 没有递归，用一个数组当栈**｜GNU coreutils · du 9.12

目录可以嵌套几十上百层。`du` 的写法不是函数递归，那它靠什么记住「每一层目前累计了多少」？

## A
**背景。** 递归写法每深一层就多一个栈帧（函数调用时存局部变量的内存），调用栈有大小上限，嵌套太深会崩。

**结构。** `du` 在一个循环里不停向遍历库要「下一个条目」，自己只维护数组 `dulvl[层号]`：每层两个累加器，一个是这一层条目之和，一个是已离开的子目录合计。深度变化时：往下走，新层清零；往上回一层，就把下层的合计加进上层。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="147" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">本层条目</text>
<text x="223" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">子目录合计</text>
<text x="36" y="51" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">dulvl[0]</text>
<rect x="112" y="34" width="70" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="147" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ent</text>
<rect x="188" y="34" width="70" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="223" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">subdir</text>
<text x="36" y="101" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">dulvl[1]</text>
<rect x="112" y="84" width="70" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="147" y="101" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ent</text>
<rect x="188" y="84" width="70" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="223" y="101" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">subdir</text>
<text x="36" y="151" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">dulvl[2]</text>
<rect x="112" y="134" width="70" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="147" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">ent</text>
<rect x="188" y="134" width="70" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="223" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">subdir</text>
<line x1="223" y1="134" x2="223" y2="118" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M223,112 L226,118 L220,118 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="223" y1="84" x2="223" y2="68" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M223,62 L226,68 L220,68 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="170" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">回到上一层时 下层的合计加进上层的 subdir</text>
</svg>
```

**细节。**

- 往下一次可能跳好几层，中间的层全部清零
- 数组按最大深度在堆上按需扩大，深度只受内存限制

**为什么。** 栈由自己管，不占调用栈；代价是要自己处理「进入」和「离开」的时机。

**例题：** LC 543 二叉树的直径（同类：LC 110 平衡二叉树）

返回二叉树的直径：任意两个结点之间最长路径的边数，路径不必经过根。结点数 `[1, 10^4]`。例：`[1,2,3,4,5]` → `3`。下面的解答用显式栈做后序，避免深树时递归爆栈。

```python
def diameter_of_binary_tree(root: TreeNode | None) -> int:
    if root is None:
        return 0
    height: dict[TreeNode, int] = {}             # 结点 -> 以它为根的子树高度（按结点数）
    best = 0
    stack: list[tuple[TreeNode, bool]] = [(root, False)]
    while stack:                                 # 迭代后序：孩子都算完再算自己，避免深树时递归爆栈
        node, visited = stack.pop()
        if not visited:
            stack.append((node, True))
            if node.left:
                stack.append((node.left, False))
            if node.right:
                stack.append((node.right, False))
        else:
            lh = height.get(node.left, 0)        # 空孩子不在字典里，高度记 0
            rh = height.get(node.right, 0)
            height[node] = 1 + max(lh, rh)
            best = max(best, lh + rh)            # 经过 node 的最长路径的边数 = 左高 + 右高
    return best
```
