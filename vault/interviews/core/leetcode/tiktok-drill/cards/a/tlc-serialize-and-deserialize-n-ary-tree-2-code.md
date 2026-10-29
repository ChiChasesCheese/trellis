---
id: tlc-serialize-and-deserialize-n-ary-tree-2-code
node: a.serialize-and-deserialize-n-ary-tree
type: qa
step: 2
---
## Q
**LC 428 序列化和反序列化 N 叉树**｜写出 Python 实现

写 `Codec` 类：`serialize(root: Node | None) -> str` 与 `deserialize(data: str) -> Node | None`，结点有 `val` 和 `children: list[Node]`。结点数 `0..10^4`，`0 <= val <= 10^4`，树高至多 `1000`，不允许用类成员 / 全局变量存状态。

## A
**思路。** 序列化：显式栈做先序，每弹出一个结点就输出 `值 孩子数`，再把孩子反向压栈使最左孩子先出。反序列化：从 token 流读根；用两个并行列表记录当前链上的结点和「还缺几个孩子」，缺口为 0 就弹栈，否则读下一个 `值 孩子数`，建结点挂到栈顶结点下并入栈。

```python
class Codec:
    def serialize(self, root: Node | None) -> str:
        if root is None:
            return ""
        out: list[str] = []
        stack = [root]
        while stack:                              # 迭代先序，树高 1000 也不会爆递归栈
            node = stack.pop()
            out.append(f"{node.val} {len(node.children)}")   # 值 + 孩子个数
            stack.extend(reversed(node.children))            # 反着压，左孩子先弹出
        return " ".join(out)

    def deserialize(self, data: str) -> Node | None:
        if not data:
            return None
        tokens = map(int, data.split())
        root = Node(next(tokens), [])
        nodes, left = [root], [next(tokens)]      # 当前链上的结点，及各自还缺几个孩子
        while nodes:
            if left[-1] == 0:                     # 孩子收齐了，回到父结点
                nodes.pop()
                left.pop()
                continue
            left[-1] -= 1
            child = Node(next(tokens), [])
            nodes[-1].children.append(child)
            nodes.append(child)
            left.append(next(tokens))
        return root
```

运行：`serialize([1,null,3,2,4,null,5,6])` → `'1 3 3 2 5 0 6 0 2 0 4 0'`，`deserialize 再按层序输出` → `[1, None, 3, 2, 4, None, 5, 6]`，`示例 1 来回一趟后与原数组相同` → `True`，`root=[]` → `('', None)`，`高 1000 的单链` → `1000`。

**复杂度。** 时间 `O(n)`：每个结点序列化时出入栈一次、反序列化时被创建一次；空间 `O(n)`（输出字符串与结点本身），额外栈 `O(h)`。字符串长度约为 `2n` 个整数。

**写法要点。** `map(int, data.split())` 返回一次性迭代器，`next(tokens)` 逐个取，不需要下标变量；`f"{node.val} {len(node.children)}"` 在一处同时写出两个字段；`stack.extend(reversed(node.children))` 一次把孩子反向压栈；`" ".join(out)` 比反复 `+=` 拼接字符串是线性的；并行列表 `nodes` / `left` 避免在栈里放可变小对象，`left[-1] -= 1` 原地改栈顶计数。所有状态都是局部变量，满足题目的无状态要求。
