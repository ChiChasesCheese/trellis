---
slug: serialize-and-deserialize-n-ary-tree
---
## Q
**LC 428 序列化和反序列化 N 叉树**｜Hard

把 N 叉树转成字符串，再还原成原树，格式自定，算法必须无状态（不能用成员变量保存状态）。

## A
**一句话。** 先序遍历，每个结点写成「值 孩子个数」，读时先读这两个数再递归建那么多棵子树，不需要分隔符或空标记。

```python
class Codec:
    def serialize(self, root):
        out = []
        def dfs(node):
            out.append(f"{node.val} {len(node.children)}")
            for kid in node.children:
                dfs(kid)
        if root:
            dfs(root)
        return " ".join(out)

    def deserialize(self, data):
        if not data:             # "".split() 是空列表
            return None
        tokens = map(int, data.split())
        def build():
            node = Node(next(tokens), [])
            for _ in range(next(tokens)):   # 读到几个孩子建几棵
                node.children.append(build())
            return node
        return build()
```

**复杂度。** 时间 `O(n)`，空间 `O(n)`。

**易错点。**
- 只存先序的值：`1→[2,3]` 与 `1→2→3` 都是 `1 2 3`，不可逆，要加孩子个数。
- 空树不判空：`"".split()` 为空，`next(tokens)` 抛 `StopIteration`。
- 把迭代器存进 `self`：题面禁止，两次调用会互相污染。

**追问。**
- 树高 1000 递归会爆吗？：会，调大递归上限，或改显式栈：序列化反着压孩子，反序列化用「结点栈加还缺几个孩子」并行栈。
- 结点值是任意字符串？：用 `json.dumps` 嵌套列表，或给 token 加长度前缀。

**同模式。** LC 297 二叉树的序列化与反序列化、LC 449 序列化和反序列化二叉搜索树、LC 331 验证二叉树的前序序列化、LC 536 从字符串生成二叉树
