---
id: tlc-serialize-and-deserialize-binary-tree-0-whole
node: a.serialize-and-deserialize-binary-tree
type: qa
---
## Q
**LC 297 二叉树的序列化与反序列化**｜Hard · LC TikTok 热度 62/100（近 6 个月） · 近一年被问：美国 2 次、国内 0 次 · CodeTop 国内累计 25 次 · 最近 2026-02-04（面试记录）

序列化是把数据结构转换为字符串（可存入文件、经网络传输），反序列化是反过来重建原结构。设计算法实现二叉树的序列化与反序列化：不限定具体格式，只需保证一棵二叉树可以被序列化为一个字符串，并且这个字符串可以被反序列化为**原始的树结构**。树中结点数在 `[0, 10^4]` 内，`-1000 <= Node.val <= 1000`。例：`root = [1,2,3,null,null,4,5]` → 序列化再反序列化后仍是 `[1,2,3,null,null,4,5]`；`root = []` → `[]`；`root = [1,2]` → `[1,2]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 层序遍历（BFS）：序列化时每个节点输出值、空位输出 `"null"`，并把两个孩子（含空）入队；反序列化时按同样的顺序，队首节点依次领走接下来的两个标记作为左右孩子。`O(n)`，不递归。

**识别。** 「设计一个编码，保证可逆」：关键是编码里要保留**结构**，不只是值。只存一种遍历序（如前序）而不标空位，无法区分形状不同的树。节点数到 `10^4`，一条链的深度也是 `10^4`，递归会栈溢出，层序可避开。

**推导。** 暴力：存中序 + 前序两个遍历序（值互不相同才可逆，题目值可重复，不可行）→ 观察：在遍历序里把每个空孩子也记成一个占位符，树和序列一一对应 → 选层序：序列化时「出队一个，写它的值，入队它的左右孩子（包括空）」，反序列化时「出队一个已建好的节点，从序列里再取两个标记当它的孩子」，两边都是循环，没有递归。

```python
from collections import deque

class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                out.append("null")                 # 空位也要占一格
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
        queue = deque([root])
        while queue:
            node = queue.popleft()
            left, right = next(tokens, "null"), next(tokens, "null")   # 每个节点后面跟着它的两个孩子位
            if left != "null":
                node.left = TreeNode(int(left))
                queue.append(node.left)
            if right != "null":
                node.right = TreeNode(int(right))
                queue.append(node.right)
        return root
```

运行：`[1,2,3,null,null,4,5]` 序列化为 `"1,2,3,null,null,4,5,null,null,null,null"`，还原后与原树逐节点一致；`[]` → `"null"`；`[1]` → `"1,null,null"`；`[1,2]` → `"1,2,null,null,null"`；`[1,null,2]` → `"1,null,2,null,null"`；一条深 `10^4` 的链往返后深度仍是 `10^4`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`（队列和输出，序列化结果含 `2n + 1` 个标记）。

**易错点。**
- 只写前序、不标空位会有歧义：根为 `1` 的两棵树，一棵只有左孩子 `2`，一棵只有右孩子 `2`，都被写成 `"1,2"`，无法区分。
- 空树要单独处理：`[]` 序列化为 `"null"`，反序列化时先判断首个标记；否则 `int("null")` 抛 `ValueError`。
- 负数和多位数：用 `str(node.val)` 与 `int(token)` 配合分隔符 `,`，不要逐字符解析，否则 `-1000` 会被拆开。

**追问。**
- 前序 + 空位标记（递归版）：写法最短，但深度等于树高，`10^4` 的链会 `RecursionError`。
- 压缩序列化结果：去掉尾部多余的 `null`；或用二进制格式存值、用位图存「是否有孩子」。
- BST 的序列化（LC 449）：不需要标空位，只存前序，利用「左 < 根 < 右」重建，序列更短。

**同模式。** LC 449 序列化和反序列化二叉搜索树、LC 428 序列化和反序列化 N 叉树、LC 105 从前序与中序遍历序列构造二叉树、LC 652 寻找重复的子树。
