---
id: tlc-construct-binary-tree-from-preorder-and-inorder-traversal-4-followup
node: b.construct-binary-tree-from-preorder-and-inorder-traversal
type: qa
step: 4
---
## Q
**LC 105 从前序与中序遍历序列构造二叉树**｜追问

面试官接着问：（1）树退化成 3000 层的链，递归栈会不会爆？不用递归怎么写？（2）改成由中序和后序构造（LC 106）要改哪里？（3）如果元素允许重复，还能唯一还原吗？

## A
1. **递归深度。** Python 默认递归上限约 1000，链状树 3000 层会抛 `RecursionError`。可以 `sys.setrecursionlimit(10000)`，或者改用显式栈的单趟算法：
```python
def build_tree_iter(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    root = TreeNode(preorder[0])
    stack = [root]
    j = 0                                   # 指向中序里下一个待“回溯”的值
    for val in preorder[1:]:
        node = stack[-1]
        if node.val != inorder[j]:          # 还没走到最左：新值是左孩子
            node.left = TreeNode(val)
            stack.append(node.left)
        else:                               # 左链走完：弹栈找到右孩子的挂载点
            while stack and stack[-1].val == inorder[j]:
                node = stack.pop()
                j += 1
            node.right = TreeNode(val)
            stack.append(node.right)
    return root
```
同样 `O(n)` 时间，没有递归，也不需要字典。
2. **LC 106。** 后序的最后一个是根，从后往前消费（`iter(reversed(postorder))`），顺序变成根、右、左，所以先建右子树再建左子树，其余不变。
3. **有重复值。** 根在中序里的位置不唯一，树不唯一，字典方法失效；题目才强调「无重复」。只给前序和后序（LC 889）同样不唯一：只有一个孩子时无法判断它是左还是右。

**Python 提醒**：`{v: i for i, v in enumerate(inorder)}` 遇到重复值时后出现的下标会覆盖先出现的，不会报错，只会悄悄建出错误的树；这类假设（无重复）要在面试里说出口。
