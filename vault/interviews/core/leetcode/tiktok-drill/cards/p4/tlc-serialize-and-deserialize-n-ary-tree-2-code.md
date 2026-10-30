---
id: tlc-serialize-and-deserialize-n-ary-tree-2-code
node: p4.serialize-and-deserialize-n-ary-tree
type: qa
step: 2
---
## Q
**LC 428 序列化和反序列化 N 叉树**｜写出 Python 实现

写 `Codec` 类：`serialize(root: Node | None) -> str` 与 `deserialize(data: str) -> Node | None`，结点有 `val` 和 `children: list[Node]`。结点数 `0..10^4`，`0 <= val <= 10^4`，树高至多 `1000`，不允许用类成员 / 全局变量存状态。

## A
**思路。** 序列化：递归先序，进入每个结点就输出 `值 孩子数`，再依次递归它的孩子。反序列化：从 token 流读 `值 孩子数` 建结点，再递归建那么多棵子树挂到它的 `children` 下。

```python
class Codec:
    def serialize(self, root: Node | None) -> str:
        out: list[str] = []

        def dfs(node: Node) -> None:
            out.append(f"{node.val} {len(node.children)}")   # 值 + 孩子个数
            for child in node.children:
                dfs(child)

        if root:
            dfs(root)
        return " ".join(out)

    def deserialize(self, data: str) -> Node | None:
        if not data:                              # 空树："".split() 是 []，必须先判空
            return None
        tokens = map(int, data.split())           # 一次性迭代器，递归调用之间共享读到哪了

        def build() -> Node:
            node = Node(next(tokens), [])
            for _ in range(next(tokens)):         # 读到几个孩子，就递归建几棵子树
                node.children.append(build())
            return node

        return build()
```

运行：`serialize([1,null,3,2,4,null,5,6])` → `'1 3 3 2 5 0 6 0 2 0 4 0'`，`deserialize 再按层序输出` → `[1, None, 3, 2, 4, None, 5, 6]`，`示例 1 来回一趟后与原数组相同` → `True`，`root=[]` → `('', None)`，`高 1000 的单链` 在默认递归上限下抛 `RecursionError`，调高上限后往返一致。

**复杂度。** 时间 `O(n)`：每个结点序列化时被访问一次、反序列化时被创建一次；空间 `O(n)`（输出字符串与结点本身），额外递归栈 `O(h)`（树高 1000 会触到默认递归上限）。字符串长度约为 `2n` 个整数。

**写法要点。** `map(int, data.split())` 返回一次性迭代器，`next(tokens)` 逐个取，不需要下标变量，递归调用之间自然共享「读到哪了」；`f"{node.val} {len(node.children)}"` 在一处同时写出两个字段；`for _ in range(next(tokens))` 直接用读到的孩子数控制递归次数；`" ".join(out)` 比反复 `+=` 拼接字符串是线性的。所有状态都是局部变量，满足题目的无状态要求。
