---
slug: serialize-and-deserialize-binary-tree
---
## Q
**LC 297 二叉树的序列化与反序列化**｜Hard

把二叉树序列化成字符串，再反序列化还原出原树，格式自定。

## A
**一句话。** 前序遍历并把空孩子写成 `#`，反序列化按同样顺序消费标记流，遇 `#` 返回空，否则先建左再建右。

```python
class Codec:
    def serialize(self, root):
        out = []
        def dfs(node):
            if not node:
                out.append("#")          # 空位也占一格
                return
            out.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(out)

    def deserialize(self, data):
        tokens = iter(data.split(","))   # 只顺序消费一次
        def build():
            tok = next(tokens)
            if tok == "#":
                return None
            node = TreeNode(int(tok))
            node.left = build()          # 先左后右，与序列化一致
            node.right = build()
            return node
        return build()
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 不标空位：只有左孩子 `2` 和只有右孩子 `2` 的两棵树都是 `"1,2"`，分不开。
- 逐字符解析：`-1000` 会被拆开，要用分隔符加 `int()`。
- 链状树深 `10^4` 会 `RecursionError`，要调大递归上限或改层序。

**追问。**
- 还有别的格式吗？：层序（BFS）加 `null`，LeetCode 的输入格式就是它。
- 值是任意字符串、可能含逗号？：对标记列表做 `json.dumps`，或加长度前缀。

**同模式。** LC 449 序列化和反序列化二叉搜索树、LC 428 序列化和反序列化 N 叉树、LC 105 从前序与中序遍历序列构造二叉树、LC 652 寻找重复的子树
