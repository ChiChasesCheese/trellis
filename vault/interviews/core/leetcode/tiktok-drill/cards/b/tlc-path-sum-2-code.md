---
id: tlc-path-sum-2-code
node: b.path-sum
type: qa
step: 2
---
## Q
**LC 112 路径总和**｜写出 Python 实现

二叉树 `root`（结点数 `0..5000`，值 `-1000..1000`，可为负）和整数 `targetSum`。判断是否存在一条从根到某个叶子的路径，其结点值之和恰好等于 `targetSum`。

## A
**思路。** `has_path_sum(node, target)` 先扣掉自己的值得到 `remain`；如果是叶子，答案就是 `remain == 0`；否则只要左子树或右子树里存在满足 `remain` 的路径就行。空树直接返回 `False`。

```python
def has_path_sum(root: TreeNode | None, target_sum: int) -> bool:
    if root is None:
        return False                   # 空树没有任何根到叶子的路径
    remain = target_sum - root.val     # 走到这里后还差多少
    if root.left is None and root.right is None:
        return remain == 0             # 必须是叶子，并且恰好凑够
    return has_path_sum(root.left, remain) or has_path_sum(root.right, remain)   # 任一侧找到就行，or 短路
```

运行：`root=[5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum=22` → `True`，`root=[1,2,3], targetSum=5` → `False`，`root=[], targetSum=0` → `False`，`root=[1,2], targetSum=1（根不是叶子）` → `False`，`root=[-2,null,-3], targetSum=-5（负数）` → `True`，`900 个结点的单链，值全为 1，targetSum=900` → `True`。

**复杂度。** 时间 `O(n)`：每个结点最多访问一次；空间 `O(h)`：递归栈深度等于树高，平衡树 `O(log n)`，退化成链 `O(n)`。

**写法要点。** 把 `target - root.val` 算成 `remain` 再往下传，叶子处只比较 `remain == 0`，比「累计和」少一个参数；`root.left is None and root.right is None` 精确表达「叶子」，比较的是结点引用，不会和 `val == 0` 的结点混淆；`or` 短路：左子树找到就不再探索右子树。深度：单链 `5000` 层会超过 CPython 默认递归上限（约 `1000`），抛 `RecursionError`，显式栈写法见追问卡。
