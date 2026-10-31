---
id: tlc-shu-de-zi-jie-gou-lcof-2-code
node: b.shu-de-zi-jie-gou-lcof
type: qa
step: 2
---
## Q
**剑指 Offer 26 树的子结构**｜写出 Python 实现

给定两棵二叉树 `tree1`、`tree2`（节点数 `0` 到 `10000`），判断 `tree2` 是否是 `tree1` 的子结构：`tree1` 中存在某个节点，以它为根向下，`tree2` 的结构和节点值都能对上，`tree1` 在对应位置多出来的孩子不影响。空树不是任何树的子结构。链状树 `10000` 层也不能报错。

## A
**思路。** 外层递归：`tree1` 当前节点作候选根调用 `match`，不行就去左子树、右子树里找。内层 `match(a, b)` 同步下降：`b` 为空这一支成功，`a` 缺节点或值不同失败，否则左右两支都要成功。

```python
def is_sub_structure(tree1: TreeNode | None, tree2: TreeNode | None) -> bool:
    def match(a: TreeNode | None, b: TreeNode | None) -> bool:    # 以 a 为根能否“包住”b
        if b is None:
            return True                      # b 这一支到头了，a 那边多出来的不管
        if a is None or a.val != b.val:
            return False                     # b 要求的节点 a 里没有，或值不同
        return match(a.left, b.left) and match(a.right, b.right)

    if tree1 is None or tree2 is None:
        return False                         # 空树不算子结构
    return (match(tree1, tree2)                         # 以 tree1 当前节点为根
            or is_sub_structure(tree1.left, tree2)      # 或者在左子树里找
            or is_sub_structure(tree1.right, tree2))    # 或者在右子树里找
```

运行：`([1,7,5], [6,1])` → `False`，`([3,6,7,1,8], [6,1])` → `True`，`(空, [1])` → `False`，`([1], 空)` → `False`，`([1,2,3], [1,2,3,4])` → `False`。

**复杂度。** 时间 `O(m * n)`（`m`、`n` 是两棵树的节点数）；空间 `O(h1 + h2)`：递归栈，深度分别是两棵树的高度，最坏 `O(m + n)`。

**写法要点。**
- `match` 先判断 `b is None`，再判断 `a is None or a.val != b.val`：顺序保证 `a.val` 访问时 `a` 非空，也让“`b` 已到头”优先于“`a` 缺节点”。
- 外层 `or` 链短路：`match(tree1, tree2)` 为真就不再往下找；`and` 连接左右两支，同样短路。
- 外层递归自己：`is_sub_structure(tree1.left, tree2)` 到了空节点会走入口的 `None` 判断返回 `False`，不需要再写单独的遍历函数；`match` 在入口之后调用，所以 `tree2` 一定非空。
- 深度：`tree1` 是 `10000` 层的链且一直找不到时，外层递归会超过 CPython 默认递归上限（约 `1000`），抛 `RecursionError`；显式栈写法见追问卡。
