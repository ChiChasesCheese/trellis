---
id: tlc-serialize-and-deserialize-binary-tree-0-whole
node: p2.serialize-and-deserialize-binary-tree
type: qa
---
## Q
**LC 297 二叉树的序列化与反序列化**｜Hard · LC TikTok 近 6 个月热度 50/100（全时段 62） · 近一年被问：美国 2 次、国内 0 次 · CodeTop 国内累计 25 次 · 最近 2026-02-04（美国面试记录）

序列化是把数据结构转换为字符串（可存入文件、经网络传输），反序列化是反过来重建原结构。设计算法实现二叉树的序列化与反序列化：不限定具体格式，只需保证一棵二叉树可以被序列化为一个字符串，并且这个字符串可以被反序列化为**原始的树结构**。树中结点数在 `[0, 10^4]` 内，`-1000 <= Node.val <= 1000`。例：`root = [1,2,3,null,null,4,5]` → 序列化再反序列化后仍是 `[1,2,3,null,null,4,5]`；`root = []` → `[]`；`root = [1,2]` → `[1,2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 前序遍历（DFS）并把空孩子也写成占位符 `"#"`：序列化是「根、左、右」递归输出；反序列化用同一个迭代器按同样顺序消费标记，读到 `"#"` 返回 `None`，否则建节点、先递归建左子树再递归建右子树。`O(n)`。

**识别。** 「设计一个编码，保证可逆」：关键是编码里要保留**结构**，不只是值。只存一种遍历序（如前序）而不标空位，无法区分形状不同的树。节点数到 `10^4`，递归 DFS 足够；一条链的深度也是 `10^4`，要留意递归上限。

**推导。** 暴力：存中序 + 前序两个遍历序（值互不相同才可逆，题目值可重复，不可行）→ 观察：在遍历序里把每个空孩子也记成一个占位符，树和序列一一对应 → 选前序：序列化时「先写根，再递归写左、右子树，空孩子写 `#`」，反序列化时「读一个标记：`#` 是空，否则建节点，递归建左、右子树」。序列里每个真实节点后面紧跟着它左、右子树的完整编码，所以不需要知道子树多大。

```python
class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []

        def dfs(node: TreeNode | None) -> None:
            if node is None:
                out.append("#")                    # 空位也要占一格
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(out)

    def deserialize(self, data: str) -> TreeNode | None:
        tokens = iter(data.split(","))             # 标记流只被顺序消费一次

        def build() -> TreeNode | None:
            tok = next(tokens)
            if tok == "#":
                return None
            node = TreeNode(int(tok))
            node.left = build()                    # 先左后右，与序列化的顺序一致
            node.right = build()
            return node

        return build()
```

运行：`[1,2,3,null,null,4,5]` 序列化为 `"1,2,#,#,3,4,#,#,5,#,#"`，还原后与原树逐节点一致；`[]` → `"#"`；`[1]` → `"1,#,#"`；`[1,2]` → `"1,2,#,#,#"`；`[1,null,2]` → `"1,#,2,#,#"`；一条深 `10^4` 的链在默认递归上限下抛 `RecursionError`，调高上限后序列化出 `20001` 个标记，还原后与原树一致。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（输出含 `2n + 1` 个标记）加 `O(h)` 的递归栈，`h` 为树高，链状树时 `O(n)`。

**拓展优化。**
- 层序（BFS）版本：两边都是循环，链状深树也不会爆递归栈；空孩子写 `"null"` 占位，读回时队首结点依次领走后面两个标记作左右孩子。

```python
from collections import deque

class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []
        queue = deque([root])                      # 空孩子也入队，才能写出 null 占位
        while queue:
            node = queue.popleft()
            if node is None:
                out.append("null")                 # 空位也要占一格，结构才能还原
                continue
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        return ",".join(out)

    def deserialize(self, data: str) -> TreeNode | None:
        tokens = iter(data.split(","))
        first = next(tokens)
        if first == "null":
            return None
        root = TreeNode(int(first))
        queue = deque([root])                      # 队里是「还没领孩子」的结点，顺序与序列化时一致
        while queue:
            node = queue.popleft()
            left, right = next(tokens, "null"), next(tokens, "null")   # 每个结点后面跟着它的两个孩子位
            if left != "null":
                node.left = TreeNode(int(left))
                queue.append(node.left)
            if right != "null":
                node.right = TreeNode(int(right))
                queue.append(node.right)
        return root
```

- 保证是二叉搜索树（BST，LC 449）时不写空位，只存先序的值，标记数从 `2n + 1` 降到 `n`；还原时用「值必须落在 `(lo, hi)` 内」判断归属。

```python
class CodecBST:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []

        def dfs(node: TreeNode | None) -> None:
            if node:
                out.append(str(node.val))          # 先序，不写空位
                dfs(node.left)
                dfs(node.right)

        dfs(root)
        return ",".join(out)

    def deserialize(self, data: str) -> TreeNode | None:
        vals = [int(x) for x in data.split(",")] if data else []
        i = 0

        def build(lo: float, hi: float) -> TreeNode | None:
            nonlocal i
            if i == len(vals) or not lo < vals[i] < hi:   # 下一个值不属于这个范围：这棵子树到此为止
                return None
            node = TreeNode(vals[i])
            i += 1
            node.left = build(lo, node.val)        # 左子树的值都小于根
            node.right = build(node.val, hi)       # 右子树的值都大于根
            return node

        return build(float("-inf"), float("inf"))
```

**易错点。**
- 只写前序、不标空位会有歧义：根为 `1` 的两棵树，一棵只有左孩子 `2`，一棵只有右孩子 `2`，都被写成 `"1,2"`，无法区分。
- 空树不能漏：`[]` 序列化为 `"#"`，`build()` 读到 `#` 直接返回 `None`；若序列化时对空根不输出占位符，反序列化 `next(tokens)` 会抛 `StopIteration`。
- 负数和多位数：用 `str(node.val)` 与 `int(token)` 配合分隔符 `,`，不要逐字符解析，否则 `-1000` 会被拆开。
- 递归深度：链状树深度为 `n = 10^4`，CPython 默认递归上限约 1000，序列化和反序列化都会抛 `RecursionError`；要么 `sys.setrecursionlimit`，要么改成不递归的层序版本（见拓展优化的层序版本）。

**追问。**
- 结点值是任意字符串（可能含逗号）：对整个标记列表做 `json.dumps`，或给每个标记加长度前缀。
- 一边读一边建、不想整串放进内存：先序版的 `tokens` 迭代器本来就只顺序消费一次，换成逐行读文件的迭代器即可。
- 压缩序列化结果：层序版本可以去掉尾部多余的 `null`；或用二进制格式存值、用位图存「是否有孩子」。

**同模式。** LC 449 序列化和反序列化二叉搜索树、LC 428 序列化和反序列化 N 叉树、LC 105 从前序与中序遍历序列构造二叉树、LC 652 寻找重复的子树。
