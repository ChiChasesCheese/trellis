---
slug: convert-bst-to-greater-tree
---
## Q
**LC 538 把二叉搜索树转换为累加树**｜Medium

给二叉搜索树，把每个节点的值改成「原树中所有大于等于它的节点值之和」。

## A
**一句话。** 反向中序（右、根、左）正好从大到小访问，边走边累加，当前节点的新值就是累计和。

```python
def convert_bst(root):
    total = 0
    def dfs(node):                      # 反向中序：右 → 根 → 左
        nonlocal total
        if not node:
            return
        dfs(node.right)
        total += node.val
        node.val = total                # 自己加上所有更大的
        dfs(node.left)
    dfs(root)
    return root
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`。

**易错点。**
- 用普通中序：从小到大访问，累加出的是「小于等于」的和，方向反了。
- 用局部变量累加：递归里的累计值要跨调用共享，用 `nonlocal` 或成员变量。
- 先改再累加：要先把原值加进 `total`，再把 `total` 写回，顺序反了会重复加。

**追问。**
- 不用递归栈？：Morris 反向中序遍历，`O(1)` 额外空间。
- 想把每个节点改成所有节点的和减去比它小的？：结果相同，只是换个角度。

**同模式。** LC 1038 从二叉搜索树到更大和树、LC 230 二叉搜索树中第K小的元素、LC 98 验证二叉搜索树、LC 501 二叉搜索树中的众数
