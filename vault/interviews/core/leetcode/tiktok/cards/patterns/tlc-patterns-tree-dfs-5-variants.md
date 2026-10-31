---
id: tlc-patterns-tree-dfs-5-variants
node: patterns.tree-dfs
type: qa
step: 5
---
## Q
**二叉树 DFS（Tree DFS）｜变形：向下传前缀和、向下传长度、返回单链增益、由遍历序列建树**

路径总和 III（LC 437）、最长连续序列（LC 298）、最大路径和（LC 124）、由前序与中序建树（LC 105）的写法各自怎样？

## A
1. **向下传前缀和 + 回溯**（例：LC 437 路径总和 III）：路径必须向下，不必从根开始。`cnt` 记录「根到当前节点这条路径上」每个前缀和出现的次数；进入节点时查 `cnt[pre - target_sum]`，离开节点的子树时要撤销 `cnt[pre] -= 1`。`[10,5,-3,3,2,null,11,3,-2,null,1], 8` → `3`；`[5,4,8,11,null,13,4,7,2,null,null,5,1], 22` → `3`。漏掉回溯：树 `[2,2,3]`、目标 `1` 得 `1`（左兄弟的前缀和泄漏过来），正确是 `0`。

2. **把当前长度向下传**（例：LC 298 二叉树最长连续序列）：`length = length + 1 if node.val == parent_val + 1 else 1`，再 `best = max(best, length)`；`[1,null,3,2,4,null,null,null,5]` → `3`。

3. **返回单链增益、在节点处合并**（例：LC 124 二叉树中的最大路径和）：每个节点返回「以它为起点向下走的最大和」（负数当 `0`），经过该节点的整条路径 = 左增益 + 右增益 + 自己，用来更新全局答案。同一个骨架也能写「好叶子对」LC 1530：返回叶子到当前节点的距离列表，在节点处把左右两个列表配对计数。

4. **由前序 + 中序建树**（例：LC 105 从前序与中序遍历序列构造二叉树）：前序的第一个是根，在中序中的位置把序列分成左右子树；用字典 `值 -> 中序下标` 做到 `O(1)` 定位，总 `O(n)`；先建左子树，因为前序里左子树排在前面。

**例题：** LC 437 路径总和 III

给二叉树的根结点 `root` 和整数 `targetSum`，求结点值之和等于 `targetSum` 的**路径**条数。路径不必从根开始、不必在叶子结束，但方向必须向下（只能从父结点走到子结点）。

```python
def path_sum(root: TreeNode | None, target_sum: int) -> int:
    prefix: Counter[int] = Counter({0: 1})       # 当前根到结点链上：前缀和 -> 出现次数

    def dfs(node: TreeNode | None, total: int) -> int:   # total：根到 node 父亲的和
        if node is None:
            return 0
        total += node.val                        # 根到 node 的和
        count = prefix[total - target_sum]       # 有多少个祖先前缀和恰好差 target_sum
        prefix[total] += 1                       # 进入：把 node 的前缀和加入当前链
        count += dfs(node.left, total) + dfs(node.right, total)
        prefix[total] -= 1                       # 离开：撤销，别的分支看不到这条链
        return count

    return dfs(root, 0)
```

**例题：** LC 298 二叉树最长连续序列

给二叉树根节点 `root`，求其中**最长连续序列路径**的长度。连续序列路径是依次递增 `1` 的路径，可以从任意节点开始，沿「父 → 子」方向向下走，不能反向。节点数在 `[1, 3 * 10^4]`，`-3 * 10^4 <= Node.val <= 3 * 10^4`。

```python
def longest_consecutive(root: TreeNode | None) -> int:
    best = 0

    def dfs(node: TreeNode, length: int) -> None:
        nonlocal best
        best = max(best, length)                 # length：以 node 结尾的连续递增路径长度
        for child in (node.left, node.right):
            if child:
                dfs(child, length + 1 if child.val == node.val + 1 else 1)

    if root:
        dfs(root, 1)
    return best
```

**例题：** LC 124 二叉树中的最大路径和

二叉树中的**路径**是一条节点序列，相邻节点之间有边，同一个节点在序列中至多出现一次；路径至少包含一个节点，不一定经过根节点。**路径和**是路径中各节点值的总和。给根节点 `root`，返回其最大路径和。树中节点数目范围 `[1, 3 * 10^4]`，`-1000 <= Node.val <= 1000`。

```python
def max_path_sum(root: TreeNode | None) -> int:
    best = root.val                                # 初值不能是 0：全负树的答案是负数

    def gain(node: TreeNode | None) -> int:        # 从 node 向下走的最大单链和；空节点贡献 0
        nonlocal best
        if node is None:
            return 0
        left = max(gain(node.left), 0)             # 负收益的子树直接不要
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)  # 以 node 为最高点的路径：两侧都可以带
        return node.val + max(left, right)         # 往父亲返回时只能选一边

    gain(root)
    return best
```

**例题：** LC 105 从前序与中序遍历序列构造二叉树

给两个整数数组 `preorder`（二叉树的前序遍历）和 `inorder`（同一棵树的中序遍历），构造这棵二叉树并返回根节点。`1 <= preorder.length <= 3000`，`inorder.length == preorder.length`，`-3000 <= preorder[i], inorder[i] <= 3000`，两个数组都**无重复元素**，且输入保证合法。

```python
def build_tree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    index = {v: i for i, v in enumerate(inorder)}   # 值 -> 中序下标
    pre = iter(preorder)                            # 前序序列只会被顺序消费一次

    def build(lo: int, hi: int) -> TreeNode | None:  # 还原中序区间 inorder[lo:hi]
        if lo == hi:
            return None
        val = next(pre)                              # 前序的下一个值就是这段的根
        mid = index[val]
        node = TreeNode(val)
        node.left = build(lo, mid)                   # 必须先建左再建右，顺序和前序一致
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder))
```
