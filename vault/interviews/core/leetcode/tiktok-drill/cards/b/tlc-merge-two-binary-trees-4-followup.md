---
id: tlc-merge-two-binary-trees-4-followup
node: b.merge-two-binary-trees
type: qa
step: 4
---
## Q
**LC 617 合并二叉树**｜追问

面试官接着问：（1）不能修改输入树怎么办？（2）2000 层的链，递归深度超限怎么处理？（3）要合并 `k` 棵树呢？

## A
1. **不改输入**：每个位置新建节点，缺失的一侧当作值 0、没有孩子。
```python
def merge_trees_new(a: TreeNode | None, b: TreeNode | None) -> TreeNode | None:
    if a is None and b is None:
        return None
    return TreeNode(
        (a.val if a else 0) + (b.val if b else 0),
        merge_trees_new(a.left if a else None, b.left if b else None),
        merge_trees_new(a.right if a else None, b.right if b else None),
    )
```
这个写法会为每个节点新建对象，代价是访问两棵树的全部节点，`O(n1 + n2)`，递归深度仍等于树高。
2. **深度超限**：改显式栈（栈里放「位置相同、都存在」的节点对），或者在面试里先说明 `sys.setrecursionlimit` 只是补丁，深度很大时可能耗尽 C 栈：
```python
def merge_trees_stack(root1: TreeNode | None, root2: TreeNode | None) -> TreeNode | None:
    if root1 is None:
        return root2
    if root2 is None:
        return root1
    stack = [(root1, root2)]                 # 每项是一对位置相同、都存在的节点
    while stack:
        a, b = stack.pop()
        a.val += b.val                       # 合并结果直接写在 root1 的节点上
        if a.left is None:
            a.left = b.left                  # root1 缺左孩子：整棵挂过来（可能为 None）
        elif b.left is not None:
            stack.append((a.left, b.left))   # 两边都有：继续往下合并
        if a.right is None:
            a.right = b.right
        elif b.right is not None:
            stack.append((a.right, b.right))
    return root1
```
两条 2000 个节点的链 → 合并出 `2000` 个节点，不抛 `RecursionError`。
3. **`k` 棵树**：逐棵合并，每次只走重叠部分，总代价不超过各树节点数之和。

**Python 提醒**：默认递归上限是 `sys.getrecursionlimit() == 1000`，一条 2000 个节点的链用递归会直接抛 `RecursionError`。
