---
id: tlc-binary-tree-inorder-traversal-4-followup
node: b.binary-tree-inorder-traversal
type: qa
step: 4
---
## Q
**LC 94 二叉树的中序遍历**｜追问

面试官接着问：（1）进阶：用迭代代替递归，深链也不能爆栈？（2）能不能不用栈，`O(1)` 额外空间？（3）只想要前 `k` 个值，前序、后序怎么改？

## A
1. **显式栈**：递归深度等于树高，链状大树会超过 CPython 默认递归上限（约 `1000`）。自己维护栈：从当前结点一路向左把沿途结点压栈，到头后弹出一个结点并访问它，然后转向它的右子树。栈里自底向顶是「已经下潜经过、还没访问」的祖先，每个结点入栈出栈各一次，`O(n)` 时间，`O(h)` 空间：

```python
def inorder_stack(root: TreeNode | None) -> list[int]:
    result: list[int] = []
    stack: list[TreeNode] = []
    node = root
    while node or stack:
        while node:                    # 一路向左，沿途结点都等着“左子树完成后”再访问
            stack.append(node)
            node = node.left
        node = stack.pop()             # 最左的结点：左子树已处理完
        result.append(node.val)        # 访问自己
        node = node.right              # 然后处理右子树
    return result
```

循环条件必须是 `while node or stack`：只写 `while stack` 时，根结点入栈前栈是空的，循环进不去。把访问放到压栈时得到的是前序。

2. **莫里斯遍历**：对每个有左子树的结点，找到左子树里最右的结点（前驱 `pred`）。`pred.right` 为空，就让它指向当前结点（搭一条回来的线）再往左走；`pred.right` 已经指向当前结点，说明左子树走完了，拆线、访问当前结点、转向右子树。没有左子树的结点直接访问并转右。每条边最多走两次，`O(n)` 时间、`O(1)` 空间，遍历结束树恢复原样：

```python
def morris_inorder(root: TreeNode | None) -> list[int]:
    result: list[int] = []
    node = root
    while node:
        if node.left is None:
            result.append(node.val)
            node = node.right
            continue
        pred = node.left
        while pred.right and pred.right is not node:
            pred = pred.right
        if pred.right is None:         # 第一次来：给前驱搭一条回到 node 的临时线
            pred.right = node
            node = node.left
        else:                          # 第二次来：左子树已走完，拆线并访问
            pred.right = None
            result.append(node.val)
            node = node.right
    return result
```

3. **前 `k` 个 / 前序、后序**：把循环写成生成器，`result.append(node.val)` 换成 `yield node.val`，调用方用 `itertools.islice(gen, k)` 取前 `k` 个，遍历到第 `k` 个就停，只花 `O(h + k)`。前序在压栈时访问；后序可以按「根、右、左」做前序，再把结果反转。

**Python 提醒**：生成器函数里的 `yield` 让函数变成惰性序列，状态（栈和当前结点）保存在生成器对象里；`next(gen)` 取下一个，`itertools.islice(gen, k)` 取前 `k` 个而不消耗其余部分。
