---
id: tlc-tops-subtree-of-another-tree-0-whole
node: trees.subtree-of-another-tree
type: qa
---
## Q
**LC 572 另一棵树的子树**｜Easy · 全公司热度第 583 名 · Blind 75、NeetCode 150

给你两棵二叉树 `root` 和 `subRoot`，检验 `root` 中是否包含和 `subRoot` 具有相同结构和节点值的子树。树 `tree` 的一棵子树包括 `tree` 的某个节点和这个节点的**所有**后代节点；`tree` 也可以看作它自身的一棵子树。`root` 的节点数在 `[1, 2000]`，`subRoot` 的节点数在 `[1, 1000]`，节点值在 `[-10^4, 10^4]`。例：`root = [3,4,5,1,2], subRoot = [4,1,2]` → `true`；`root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]` → `false`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 树的递归比较（LC 100 相同的树）嵌在对 `root` 每个节点的 DFS 里。

**一句话。** `subRoot` 是 `root` 的子树，当且仅当存在 `root` 里的某个节点，以它为根的整棵树与 `subRoot` 完全相同。

**识别。** 「子树」要求连同所有后代一起相同，这和「子结构」不同；枚举候选根（`root` 的每个节点），对每个候选做一次「相同的树」比较。`m = 2000`、`n = 1000`，`O(mn)` 最多 `2 * 10^6` 次比较，足够。

**推导。** 做法分两层：外层 DFS 访问 `root` 的每个节点当候选根，内层 `same` 判断两棵树是否完全相同。内层遇到值不同或结构不同就提前返回，实际很快。

```python
def is_subtree(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    def same(a: TreeNode | None, b: TreeNode | None) -> bool:
        if a is None or b is None:
            return a is b                          # 同为空才相同
        return a.val == b.val and same(a.left, b.left) and same(a.right, b.right)

    if root is None:
        return False                               # 候选根用完了
    return (same(root, sub_root)                   # 以 root 为根是否恰好等于 sub_root
            or is_subtree(root.left, sub_root)     # 否则去左右子树里找
            or is_subtree(root.right, sub_root))
```

运行：`[3,4,5,1,2]` 与 `[4,1,2]` → `True`；`[3,4,5,1,2,null,null,null,null,0]` 与 `[4,1,2]` → `False`；`[1,1]` 与 `[1]` → `True`；`[1]` 与 `[2]` → `False`。

**复杂度。** 时间 `O(mn)`，`m`、`n` 为两棵树的节点数；空间 `O(h)`，递归栈。

**拓展优化。**
- 序列化后做子串匹配：把每棵树按先序、带空节点标记序列化成字符串，`sub` 的串是 `root` 的串的子串，当且仅当是子树。每个值前加分隔符，否则 `12` 与 `2` 会误配。
```python
def is_subtree_serialize(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    def ser(node: TreeNode | None) -> str:
        if node is None:
            return "$"                             # 空节点标记，保留结构
        return f"#{node.val},{ser(node.left)}{ser(node.right)}"   # '#' 标出数值起点

    return ser(sub_root) in ser(root)
```
  Python 的 `in` 对子串匹配平均很快；要严格 `O(m + n)` 可换 KMP，或用 Merkle 哈希（每个子树哈希成一个 id，比较 id）。

**易错点。**
- 只比较 `root` 与 `subRoot` 的根：`[3,4,5,1,2]` 与 `[4,1,2]` 得 `False`，正确是 `True`。要对每个节点都试一次。
- 内层比较只检查 `sub` 非空的部分、不检查 `root` 那侧是否还有多余后代：示例 2 里 `root` 的 `4→1` 下面多了一个 `0`，`sub` 的 `1` 是叶子，这种写法会判 `True`，正确是 `False`。子树要求整棵相同，空与非空必须不等。
- 链状树的递归深度可达 `2000`，超过 CPython 默认上限约 `1000`，需调高。

**同模式。** LC 100 相同的树、LC 101 对称二叉树、LC 652 寻找重复的子树、LC 1367 二叉树中的链表。
