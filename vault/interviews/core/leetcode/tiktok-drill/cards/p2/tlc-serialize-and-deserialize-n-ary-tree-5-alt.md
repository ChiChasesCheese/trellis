---
id: tlc-serialize-and-deserialize-n-ary-tree-5-alt
node: p2.serialize-and-deserialize-n-ary-tree
type: qa
step: 5
---
## Q
**LC 428 序列化和反序列化 N 叉树**｜另一种解法

「先序 + 孩子数」的递归写法在高 1000 的链上会爆栈，不递归的版本怎么写？还有别的编码吗？什么时候选哪一种？

## A
**解法二：显式栈，同样的编码。** 序列化用栈做先序，反着压孩子使左孩子先出；反序列化用「结点栈 + 还缺几个孩子」的并行栈，缺口为 0 就弹栈。深度无关，高 1000 的链也不会 `RecursionError`：

```python
class CodecStack:
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

并行列表 `nodes` / `left` 记录当前链上的结点和各自还缺的孩子数，`left[-1] -= 1` 原地改栈顶计数。运行：`'1 3 3 2 5 0 6 0 2 0 4 0'` 还原后按层序输出 `[1, None, 3, 2, 4, None, 5, 6]`；高 1000 的单链往返一致。

**解法三：层序 + `null` 分隔**（题面给的格式）：BFS，每个结点的孩子写完后写一个 `null`。解码用队列，按顺序给队首结点分配孩子，不会递归，深度无关；缺点是 `null` 让输出更长，需要区分「值」与「空标记」。

**怎么选。** 面试里先写递归版（`10` 行，讲清编码思想），然后主动说「高 1000 会爆栈」并给出本卡的显式栈版本，是最稳的路径；要和 LeetCode 的输入格式互转时用层序版。
