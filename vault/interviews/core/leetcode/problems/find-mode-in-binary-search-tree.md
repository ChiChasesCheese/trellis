---
slug: find-mode-in-binary-search-tree
---
## Q
**LC 501 二叉搜索树中的众数**｜Easy

给含重复值的二叉搜索树（左子树 `≤` 根 `≤` 右子树），返回出现次数最多的所有值（众数），要求额外空间不超过 `O(1)`（不计递归栈）。

## A
**一句话。** 中序遍历 BST 得到有序序列，相同的值必然挨在一起，边走边数当前值的连续次数，与最高频比较。

```python
def find_mode(root):
    ans, best, cnt, prev = [], 0, 0, None
    def dfs(node):                    # 中序：值有序
        nonlocal best, cnt, prev
        if not node:
            return
        dfs(node.left)
        cnt = cnt + 1 if node.val == prev else 1
        prev = node.val
        if cnt > best:
            best, ans[:] = cnt, [node.val]   # 刷新最高频
        elif cnt == best:
            ans.append(node.val)
        dfs(node.right)
    dfs(root)
    return ans
```

**复杂度。** 时间 `O(n)`，空间 `O(h)`（递归栈），不计答案。

**易错点。**
- 用哈希表计数：能过，但违背「`O(1)` 额外空间」，也没用上 BST 的有序性。
- `cnt > best` 时不清空答案：旧的众数会残留，要重置成只含当前值。
- 当前值与前一个值不同却不把 `cnt` 重置为 `1`：不同值会累加成一个计数。

**追问。**
- 需要不用递归栈的 `O(1)` 空间怎么办？：Morris 中序遍历，临时把前驱的右指针指回当前节点，遍历完再恢复。
- 普通二叉树呢？：中序不再有序，只能用哈希表计数，`O(n)` 空间。

**同模式。** LC 530 二叉搜索树的最小绝对差、LC 783 二叉搜索树节点最小距离、LC 98 验证二叉搜索树、LC 230 二叉搜索树中第K小的元素
