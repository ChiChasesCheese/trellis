---
slug: two-sum-iv-input-is-a-bst
---
## Q
**LC 653 两数之和 IV - 输入二叉搜索树**｜Easy

给二叉搜索树和目标值 `k`，判断树中是否存在两个不同节点，值之和等于 `k`。

## A
**一句话。** 遍历时用哈希集合记下已见过的值，对每个节点查 `k - 值` 是否已在集合里。

```python
def find_target(root, k):
    seen = set()
    def dfs(node):
        if not node:
            return False
        if k - node.val in seen:         # 互补数之前出现过
            return True
        seen.add(node.val)
        return dfs(node.left) or dfs(node.right)
    return dfs(root)
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 先加入集合再查：会把节点自己当成互补数（`2k = val` 时误判），要先查后加。
- 对两个不同节点：同一个节点不能用两次，所以要先查后加。
- 只在左右子树里分别找：数对可以跨左右子树，集合要全局共享。

**追问。**
- 利用 BST 有序性，省空间的做法？：中序得到有序数组再双指针，或两个中序迭代器（正向、反向）同时走，`O(h)` 空间。
- 为什么哈希集合不用到 BST 性质？：这是通用的两数之和，BST 的优势在于有序版本。

**同模式。** LC 1 两数之和、LC 167 两数之和 II - 输入有序数组、LC 15 三数之和、LC 98 验证二叉搜索树
