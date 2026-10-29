---
id: tlc-subtree-of-another-tree-0-whole
node: a.subtree-of-another-tree
type: qa
---
## Q
**LC 572 另一个树的子树**｜Easy · 字节高频

给两棵二叉树 `root` 和 `subRoot`，判断 `root` 中是否存在一棵子树，结构和节点值都与 `subRoot` 完全相同。子树指某个节点连同它的全部后代；`root` 自己也算自己的子树。`root` 的节点数在 `[1, 2000]`，`subRoot` 的节点数在 `[1, 1000]`，节点值在 `[-10^4, 10^4]`。例：`root = [3,4,5,1,2]`、`subRoot = [4,1,2]` → `true`；`root = [3,4,5,1,2,null,null,null,null,0]` → `false`（`4` 的后代里多了一个 `0`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 把两棵树各自先序序列化成字符串（空孩子记 `#`，每个值前加逗号），子树等价于「`subRoot` 的序列是 `root` 序列的子串」，一次 `in` 判断即可。`O(m + n)`。

**识别。** 「树里是否含有某个形状的子树」= 子结构匹配；两条路：对每个候选根做「两树是否完全相同」比较（`O(m·n)`），或把树压成序列后做字符串匹配。`root` 深度可达 `2000`，递归会超过 Python 默认的 `1000` 层，所以序列化要用显式栈。

**推导。** 暴力：枚举 `root` 的每个节点，判断以它为根的子树是否与 `subRoot` 相同，最坏 `O(m·n)` → 浪费在每个候选都要重新比较 → 洞察：先序序列加上空位记号能唯一确定一棵树的形状和值，于是「子树匹配」变成「子串匹配」→ 值前面加逗号分隔，防止 `"12"` 里匹配出 `"2"` → 两次迭代先序加一次 `in`，线性。

```python
def is_subtree(root: TreeNode | None, sub_root: TreeNode | None) -> bool:
    def serialize(tree: TreeNode | None) -> str:
        parts: list[str] = []
        stack = [tree]                             # 迭代先序，避免深链表式的树爆递归栈
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

运行：示例 1 → `True`，示例 2 → `False`；深度 2000 的右链里找深度 1000 的右链 → `True`，左链里找右链 → `False`。

**复杂度。** 序列化 `O(m + n)`；子串判断 `str.__contains__`：CPython 3.10 起对长模式用双向算法（two-way），最坏线性，所以总时间 `O(m + n)`，空间 `O(m + n)`。

**易错点。**
- 不加分隔符：`root = [12]`、`subRoot = [2]` 的序列是 `"12##"` 与 `"2##"`，`"2##"` 是子串，输出 `True`，正确是 `False`。
- 不记空位：`root = [1,2]`（`2` 是左孩子）与 `subRoot = [1,null,2]`（`2` 是右孩子）去掉空位记号后的序列都是 `",1,2"`，输出 `True`，正确是 `False`。
- 子树必须连后代一起相同：示例 2 里 `4` 的后代多了一个 `0`，所以不算；序列化里的 `#` 正好承担「到叶子为止」这一点。

**追问。**
- 不想用字符串：对每个值等于 `subRoot.val` 的节点，用显式栈逐对比较，`O(m·n)`，空间 `O(h)`。
- 想要稳定的 `O(m + n)`：先序序列用 KMP；或者给每个子树算结构哈希（Merkle 哈希），对比哈希。
- 判断两棵树是否相同（LC 100）是这个问题的子问题，最简单的递归就是 `a.val == b.val and same(a.left, b.left) and same(a.right, b.right)`。

**同模式。** LC 100 相同的树、LC 652 寻找重复的子树、LC 1367 链表中的二叉树路径、LC 297 二叉树的序列化与反序列化。
