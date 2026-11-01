---
id: tlc-tops-serialize-and-deserialize-binary-tree-0-whole
node: trees.serialize-and-deserialize-binary-tree
type: qa
---
## Q
**LC 297 二叉树的序列化与反序列化**｜Hard · 全公司热度第 114 名 · Blind 75、NeetCode 150

序列化是把一个数据结构转换成一个字符串，使它可以存储或在网络上传输，并且之后能被还原。设计一个算法实现二叉树的序列化与反序列化：不限定序列化的逻辑，只需保证一棵二叉树可以被序列化成一个字符串，并且该字符串可以被反序列化成**原来的树**。实现类 `Codec`，包含 `serialize(root) -> str` 和 `deserialize(data) -> TreeNode | None`。节点数在 `[0, 10^4]`，`-1000 <= Node.val <= 1000`。例：`root = [1,2,3,null,null,4,5]` → 序列化再反序列化后仍是 `[1,2,3,null,null,4,5]`；`root = []` → `[]`；`root = [1,2]` → `[1,2]`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 带空节点标记的先序遍历（DFS）：序列化是遍历，反序列化是用同一个遍历顺序重建。

**一句话。** 先序遍历输出，空节点输出占位符 `#`，逗号分隔；反序列化时按同样的先序顺序逐个读取：读到 `#` 返回空，否则建节点并先建左再建右。

**识别。** 「树 ↔ 字符串」：单独的先序（或中序）序列不能唯一确定树，必须带空节点标记，把形状信息写进去。设计题不限格式，选最容易写对的：先序加占位符，序列化与反序列化是同一个递归结构的两面。`n <= 10^4`，`O(n)`。

**推导。** 一种做法是同时存先序和中序再还原（LC 105），要求无重复值且字符串翻倍。带空节点标记的先序已经足够：每个节点后面必然紧跟它的整棵左子树和整棵右子树（空子树用 `#` 占一个位置），读到的 `#` 恰好终止一条递归路径，所以反序列化无需记下标。

```python
class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []

        def dfs(node: TreeNode | None) -> None:
            if node is None:
                out.append("#")                    # 空节点占位，保留形状
                return
            out.append(str(node.val))              # 先序：根、左、右
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(out)

    def deserialize(self, data: str) -> TreeNode | None:
        tokens = iter(data.split(","))             # 迭代器：按先序顺序一个一个消费

        def build() -> TreeNode | None:
            token = next(tokens)
            if token == "#":
                return None                        # 空节点：这条递归路径结束
            node = TreeNode(int(token))
            node.left = build()                    # 先左后右，与序列化顺序一致
            node.right = build()
            return node

        return build()
```

运行：`[1,2,3,null,null,4,5]` → 序列化为 `1,2,#,#,3,4,#,#,5,#,#`，还原后仍是 `[1,2,3,null,null,4,5]`；`[]` → `#` → `[]`；`[1,2]` → `1,2,#,#,#` → `[1,2]`；`[-1,null,-2]` → `-1,#,-2,#,#` → `[-1,null,-2]`。

**复杂度。** 时间 `O(n)`，两个方向都是；空间 `O(n)`，字符串与递归栈。

**拓展优化。**
- 层序（BFS）版，格式和 LeetCode 的 `[1,2,3,null,null,4,5]` 一致，不用递归，天然适合深链树：
```python
from collections import deque

class CodecBFS:
    def serialize(self, root: TreeNode | None) -> str:
        out: list[str] = []
        queue = deque([root])
        while queue:
            node = queue.popleft()
            if node is None:
                out.append("#")
                continue
            out.append(str(node.val))
            queue.append(node.left)
            queue.append(node.right)
        return ",".join(out)

    def deserialize(self, data: str) -> TreeNode | None:
        tokens = data.split(",")
        if tokens[0] == "#":
            return None
        root = TreeNode(int(tokens[0]))
        queue = deque([root])
        i = 1
        while queue:
            node = queue.popleft()
            if tokens[i] != "#":                   # 每个出队节点依次消费两个 token：左孩子、右孩子
                node.left = TreeNode(int(tokens[i]))
                queue.append(node.left)
            i += 1
            if tokens[i] != "#":
                node.right = TreeNode(int(tokens[i]))
                queue.append(node.right)
            i += 1
        return root
```

**易错点。**
- 不写空节点标记：`[1,2]`（2 是左孩子）与 `[1,null,2]`（2 是右孩子）的先序都是 `1,2`，还原时无法区分。
- 不用分隔符，直接拼接数字：`12` 分不清是 `1,2` 还是 `12`；负数的 `-` 号也要保留。必须用逗号分隔。
- 链状树深度 `10^4`，远超 CPython 默认递归上限约 `1000`，序列化与反序列化都会抛 `RecursionError`；需调高上限或用上面的 BFS 版。

**同模式。** LC 105 从前序与中序遍历序列构造二叉树、LC 449 序列化和反序列化二叉搜索树、LC 428 序列化和反序列化 N 叉树、LC 652 寻找重复的子树。
