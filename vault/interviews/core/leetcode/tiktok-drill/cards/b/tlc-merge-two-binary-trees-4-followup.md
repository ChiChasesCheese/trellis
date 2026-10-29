---
id: tlc-merge-two-binary-trees-4-followup
node: b.merge-two-binary-trees
type: qa
step: 4
---
## Q
**LC 617 合并二叉树**｜追问

面试官接着问：（1）不能修改输入树怎么办？（2）递归写法深度超限怎么处理？（3）要合并 `k` 棵树呢？

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
2. **深度超限**：改显式栈（主解法），或者在面试里先说明 `sys.setrecursionlimit` 只是补丁，深度很大时可能耗尽 C 栈。
3. **`k` 棵树**：逐棵合并，每次只走重叠部分，总代价不超过各树节点数之和。

**Python 提醒**：默认递归上限是 `sys.getrecursionlimit() == 1000`，一条 2000 个节点的链用递归会直接抛 `RecursionError`。
