---
slug: binary-tree-inorder-traversal
---
## Q
**LC 94 二叉树的中序遍历**｜Easy

给定一个二叉树的根节点 `root`，返回它的**中序**遍历（左、根、右）。节点数在 `[0, 100]`，`-100 <= Node.val <= 100`。例：`root = [1,null,2,3]` → `[1,3,2]`；`root = []` → `[]`；`root = [1]` → `[1]`。进阶：递归算法很简单，你可以通过迭代算法完成吗？

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 二叉树深度优先遍历三种顺序（前、中、后序）；递归与显式栈的对应。

**一句话。** 中序 = 先遍历左子树，再访问当前节点，最后遍历右子树；递归把这句话直接翻译成代码。

**识别。** 「按某种顺序输出树的所有节点」就是 DFS 遍历，顺序只取决于「访问自己」这一行放在两次递归的前、中、后。二叉搜索树（BST）的中序遍历是升序，这是遍历题和 BST 题的接口。`n <= 100`，递归没有任何压力。

**推导。** 访问顺序由递归结构本身给出：只要把 `res.append(node.val)` 放在左右递归之间就是中序。进阶要求迭代，是因为递归的本质是系统栈，自己维护一个栈就能模拟（见拓展优化）。

```python
def inorder_traversal(root: TreeNode | None) -> list[int]:
    res: list[int] = []

    def dfs(node: TreeNode | None) -> None:
        if node is None:
            return                                 # 空节点：什么也不做
        dfs(node.left)                             # 左
        res.append(node.val)                       # 根：夹在两次递归之间就是中序
        dfs(node.right)                            # 右

    dfs(root)
    return res
```

运行：`[1,null,2,3]` → `[1, 3, 2]`；`[]` → `[]`；`[1]` → `[1]`；`[2,1,3]` → `[1, 2, 3]`。

**复杂度。** 时间 `O(n)`；空间 `O(h)`（递归栈，不含输出）。

**拓展优化。**
- 迭代（进阶）：一路向左压栈，走到头弹出访问，再转向右子树。
```python
def inorder_traversal_iter(root: TreeNode | None) -> list[int]:
    res: list[int] = []
    stack: list[TreeNode] = []
    node = root
    while node or stack:
        while node:                                # 一路向左，沿途的节点等左子树处理完再访问
            stack.append(node)
            node = node.left
        node = stack.pop()                         # 左边走完了，弹出的就是下一个要访问的节点
        res.append(node.val)
        node = node.right                          # 然后处理它的右子树
    return res
```
- Morris 遍历，`O(1)` 额外空间：把当前节点挂到左子树最右节点的右指针上当作「返回路标」，访问后再拆掉。

```python
def inorder_traversal_morris(root: TreeNode | None) -> list[int]:
    res: list[int] = []
    node = root
    while node:
        if node.left is None:
            res.append(node.val)                   # 没有左子树：直接访问，转向右
            node = node.right
            continue
        pred = node.left
        while pred.right and pred.right is not node:
            pred = pred.right                      # 找中序前驱：左子树最右的节点
        if pred.right is None:
            pred.right = node                      # 第一次到达：搭路标，进入左子树
            node = node.left
        else:
            pred.right = None                      # 第二次到达：左子树已处理完，拆路标
            res.append(node.val)
            node = node.right
    return res
```

**易错点。**
- 把 `res.append` 放错位置：放在两次递归之前得到前序，`[1,null,2,3]` 输出 `[1,2,3]`；放在之后得到后序 `[3,2,1]`；中序是 `[1,3,2]`。
- 迭代版里弹出节点后忘记转向右子树（`node = node.right`），死循环或漏掉右半边。
- 链状树的递归深度可达 `n`，CPython 默认上限约 `1000`；这里 `n <= 100` 安全，输入更大时用迭代版。

**同模式。** LC 98 验证二叉搜索树（中序严格递增）、LC 230 二叉搜索树中第 K 小的元素、LC 144 前序遍历、LC 145 后序遍历。
