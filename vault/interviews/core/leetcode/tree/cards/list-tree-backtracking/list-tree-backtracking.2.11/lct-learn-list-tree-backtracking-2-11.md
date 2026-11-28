---
id: lct-learn-list-tree-backtracking-2-11
node: list-tree-backtracking.2.11
type: qa
step: 1
---
## Q
**链表、二叉树与回溯 › 二叉树 › 插入/删除节点**｜学习卡

套路是什么？

## A
**一句话。** 增删改树用「函数返回这棵子树新的根」：每层写 `node.left = f(node.left)` 接住返回值，插入、删除、修剪是同一个递归外壳，区别只在命中时返回什么。

下图：插入、删除、修剪共用同一个外壳，区别只在命中时返回什么。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<rect x="62.8" y="7.5" width="214.5" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="24.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f(node, key) 返回这棵子树新的根</text>
<polygon points="95.3,66.0 104.3,53.5 235.7,53.5 244.7,66.0 235.7,78.5 104.3,78.5" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="70.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">比较 key 与 node.val</text>
<rect x="5.2" y="102.0" width="99.5" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="55" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">node.left =</text>
<text x="55" y="133.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f(node.left)</text>
<rect x="231.8" y="102.0" width="106.5" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="285" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">node.right =</text>
<text x="285" y="133.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f(node.right)</text>
<rect x="111.1" y="102.0" width="117.8" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="170" y="118.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">命中：返回替身</text>
<text x="170" y="133.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">右 / 左 / 后继值</text>
<rect x="25.0" y="179.5" width="290" height="25" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="196.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">其余路径 return node：赋值不改指针</text>
<path d="M 170.0 32.5 L 170.0 53.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,53.5 167.0,47.2 173.0,47.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 95.3 66.0 L 55.0 66.0 L 55.0 102.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="55.0,102.0 52.0,95.7 58.0,95.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="80" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">&lt;</text>
<path d="M 244.7 66.0 L 285.0 66.0 L 285.0 102.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="285.0,102.0 282.0,95.7 288.0,95.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="260" y="60" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">&gt;</text>
<path d="M 170.0 78.5 L 170.0 102.0" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,102.0 167.0,95.7 173.0,95.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178.0" y="94.2" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">=</text>
<path d="M 55.0 142.0 L 55.0 179.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="55.0,179.5 52.0,173.2 58.0,173.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<path d="M 285.0 142.0 L 285.0 179.5" fill="none" stroke-width="1.2" stroke="currentColor"/>
<polygon points="285.0,179.5 282.0,173.2 288.0,173.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
</svg>

```python
def delete_node(root, key):          # LC 450
    if root is None:
        return None                  # 没找到：什么也不做
    if key < root.val:
        root.left = delete_node(root.left, key)    # 接住返回值
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right        # 无左孩子：右子树顶替自己
        if root.right is None:
            return root.left
        succ = root.right            # 两个孩子：找中序后继
        while succ.left:
            succ = succ.left         # 右子树里最小的
        root.val = succ.val          # 值顶上来，再删后继
        root.right = delete_node(root.right, succ.val)
    return root                      # 路径上原样返回，赋值不改指针
```

**要点。**
- 为什么对？：契约是「返回处理完的子树的根」，孩子被删或被换人父亲都不用特判；叶子和单孩子都归到前两个 `return`。
- 两个孩子为什么用中序后继？：右子树最小节点比 `x` 大、比右子树其余都小，正好顶替；它没有左孩子，再删它只会落入简单情形。
- LC 701、LC 669 怎么改？：701 在空位返回 `TreeNode(val)`；669 节点太小返回修剪后的右子树，太大返回左子树，否则保留自己并修剪两边。

**易错点。**
- 没接返回值：写成 `delete_node(root.left, key)`，父亲仍指着旧节点；`[5,3,6,2,4,null,7]`、`key = 3` 应得合法 BST 如 `[5,4,6,2,null,null,7]`。
- 两个孩子只复制值、不删后继：树里出现两个相同的值。
- `key` 不存在：`[2,1,3]`、`key = 5` 应原样返回，空树返回空。

**对应题目。** LC 450 删除二叉搜索树中的节点
