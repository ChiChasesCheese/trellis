---
id: tlc-subtree-of-another-tree-0-whole
node: p3.subtree-of-another-tree
type: qa
---
## Q
**LC 572 另一个树的子树**｜Easy · 近一年被问：美国 0 次、国内 5 次 · CodeTop 国内累计 24 次 · 最近 2026-10-17（国内面试记录）

给两棵二叉树 `root` 和 `subRoot`，判断 `root` 中是否存在一棵子树，结构和节点值都与 `subRoot` 完全相同。子树指某个节点连同它的全部后代；`root` 自己也算自己的子树。`root` 的节点数在 `[1, 2000]`，`subRoot` 的节点数在 `[1, 1000]`，节点值在 `[-10^4, 10^4]`。例：`root = [3,4,5,1,2]`、`subRoot = [4,1,2]` → `true`；`root = [3,4,5,1,2,null,null,null,null,0]` → `false`（`4` 的后代里多了一个 `0`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 对 `root` 的每个节点做一次「两棵树是否完全相同」的比较，只要有一个节点命中就是 `True`；「相同」自己也是一个递归：两个根值相等，左对左、右对右都相同。最坏 `O(m·n)`，`m ≤ 2000`、`n ≤ 1000` 足够。

**识别。** 「树里是否含有某个形状的子树」= 子结构匹配；子树的定义本身是递归的（节点连同全部后代），所以直接把「在 `root` 中找」和「两树相同」各写成一个递归函数。想要线性时间，把树压成带空位记号的先序序列再做子串匹配（见追问）。

**推导。** 暴力：枚举 `root` 的每个节点，判断以它为根的子树是否与 `subRoot` 完全相同 → 「完全相同」是 LC 100，一个三行递归 → 外层再递归地枚举左右子树，等价于「`root` 本身相同，或 `subRoot` 是左子树的子树，或是右子树的子树」→ 每个候选最多比较 `n` 个节点，总共 `O(m·n)`，约 `2·10^6` 次，足够。

```python
def is_same(a: TreeNode | None, b: TreeNode | None) -> bool:
    if a is None or b is None:
        return a is b                              # 同时为空才算相同，只有一边为空就不同
    return a.val == b.val and is_same(a.left, b.left) and is_same(a.right, b.right)


def is_subtree(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    if root is None:
        return False                               # 走到空还没匹配上
    return is_same(root, sub_root) or is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)
```

运行：`[3,4,5,1,2]` 里找 `[4,1,2]` → `True`；`[3,4,5,1,2,null,null,null,null,0]` 里找 `[4,1,2]` → `False`；深度 2000 的右链里找深度 1000 的右链，调高递归上限后 → `True`，深度 2000 的左链里找右链 → `False`。

**复杂度。** 时间 `O(m·n)`：外层访问 `m` 个节点，每个节点上的 `is_same` 最多比较 `n` 个节点（最坏是 `root` 与 `subRoot` 都是全 `1` 的链）；空间 `O(m)`，是递归栈的深度。

**易错点。**
- 「相同」必须比到叶子为止：示例 2 里 `4` 的后代多了一个 `0`，只比较值和左右孩子是否存在会漏掉，`is_same(2, 2)` 要看到 `2` 的左孩子 `0` 对上 `subRoot` 里的空，返回 `False`。
- 只比较 `root.val == sub_root.val` 就返回：`root = [1,1]`、`subRoot = [1]`，根值相同，但 `root` 的根下面还有孩子，`is_same` 返回 `False`，再往下找到左孩子才是 `True`；少了「继续找孩子」会把答案算错。
- 递归深度：`root` 最深可以是 `2000` 个节点的链，而 CPython 默认递归上限约 `1000`，`is_subtree` 沿着链往下递归会抛 `RecursionError`；要么 `sys.setrecursionlimit` 调高，要么改成迭代（见追问）。

**追问。**
- 想要线性时间：两棵树各自先序序列化（空孩子记 `#`，每个值前加逗号），`subRoot` 的序列是 `root` 序列的子串当且仅当存在匹配子树；`in` 在 CPython 3.10 起最坏线性，总时间 `O(m + n)`，用显式栈做先序，深链也不会超过递归上限。
- 不用字符串、也不想碰递归：两个遍历都改成显式栈，`O(m·n)` 时间、`O(h)` 额外空间。
- 想要有保证的线性：先序序列用 KMP；或者给每个子树算结构哈希（Merkle 哈希），对比哈希。

```python
def is_subtree_serialize(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    def serialize(tree: TreeNode | None) -> str:
        parts: list[str] = []
        stack = [tree]
        while stack:
            node = stack.pop()
            if node is None:
                parts.append("#")                  # 空位也要记，才能区分形状
            else:
                parts.append(f",{node.val}")       # 值前加逗号，防止 "12" 里匹配出 "2"
                stack.append(node.right)
                stack.append(node.left)            # 后进先出：左子树先出栈
        return "".join(parts)

    return serialize(sub_root) in serialize(root)
```

**同模式。** LC 100 相同的树、LC 652 寻找重复的子树、LC 1367 链表中的二叉树路径、LC 297 二叉树的序列化与反序列化。
