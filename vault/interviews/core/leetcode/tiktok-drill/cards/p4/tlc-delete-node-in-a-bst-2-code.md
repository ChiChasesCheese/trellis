---
id: tlc-delete-node-in-a-bst-2-code
node: p4.delete-node-in-a-bst
type: qa
step: 2
---
## Q
**LC 450 删除二叉搜索树中的节点**｜写出 Python 实现

`TreeNode` 有 `val`、`left`、`right`。给定 BST 的根（节点数 `0` 到 `10^4`，值唯一）和 `key`，删除值为 `key` 的节点并保持 BST 性质，返回根；`key` 不存在则不变。要求 `O(h)` 时间，树可能退化成链。

## A
**思路。** 递归：`key` 小于根就去左子树删，大于根就去右子树删，把返回值接回对应的孩子指针。命中时：没有左孩子就返回右子树，没有右孩子就返回左子树（这两条已经覆盖叶子）；两个孩子时，找到右子树最左的后继，把它的值抄到目标上，再到右子树里删掉那个值。

```python
def delete_node(root: TreeNode | None, key: int) -> TreeNode | None:
    if root is None:
        return None                            # 树里没有 key
    if key < root.val:
        root.left = delete_node(root.left, key)      # 目标在左子树：删完用返回值接回来
    elif key > root.val:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            return root.right                  # 没有左孩子（含叶子）：右子树顶替自己
        if root.right is None:
            return root.left                   # 只有左孩子：左子树顶替自己
        succ = root.right                      # 两个孩子：用中序后继（右子树最小值）顶替
        while succ.left:
            succ = succ.left
        root.val = succ.val
        root.right = delete_node(root.right, succ.val)   # 再到右子树里删掉那个后继
    return root
```

运行：`[5,3,6,2,4,null,7]` 删 `3` → `[5,4,6,2,null,null,7]`；删 `0` → `[5,3,6,2,4,null,7]`；删根 `5` → `[6,3,7,2,4]`；`[]` 删 `0` → `[]`；`[1]` 删 `1` → `[]`；值为 `1` 到 `10^4` 的右斜链，调高递归上限后依次删 `5000` 和 `10000` → 剩 `9998` 个节点，默认上限下删 `10000` 抛 `RecursionError`。

**复杂度。** 时间 `O(h)`：向下找目标一条路径，找后继再一条路径；空间 `O(h)`，是递归栈。

**写法要点。** `root.left = delete_node(root.left, key)` 让每层返回「删除后的子树根」并由父节点接回，删根、删叶子都不需要父指针和特判；`if root.left is None: return root.right` 一行同时处理叶子和只有右孩子；`while succ.left` 找右子树最小值；最后一步 `delete_node(root.right, succ.val)` 复用同一个函数，后继落入「没有左孩子」的分支；链状树深度可达 `10^4`，要 `sys.setrecursionlimit` 或用「追问」卡的迭代版。
