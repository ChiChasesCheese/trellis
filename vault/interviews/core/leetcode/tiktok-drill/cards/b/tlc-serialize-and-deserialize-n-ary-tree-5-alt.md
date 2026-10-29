---
id: tlc-serialize-and-deserialize-n-ary-tree-5-alt
node: b.serialize-and-deserialize-n-ary-tree
type: qa
step: 5
---
## Q
**LC 428 序列化和反序列化 N 叉树**｜另一种解法

序列化 N 叉树除了「先序 + 孩子数」，还有别的做法吗？什么时候选哪一种？

## A
**解法二：递归先序，同样的编码。** 代码最短，适合树高有保证（比如平衡的 `h ≤ 100`）的场合：

```python
def encode(root: Node | None) -> str:
    out: list[str] = []
    def dfs(node: Node) -> None:
        out.append(f"{node.val} {len(node.children)}")
        for child in node.children:
            dfs(child)
    if root:
        dfs(root)
    return " ".join(out)

def decode(data: str) -> Node | None:
    if not data:
        return None
    tokens = map(int, data.split())
    def build() -> Node:
        node = Node(next(tokens), [])
        for _ in range(next(tokens)):
            node.children.append(build())
        return node
    return build()
```

`decode` 的 `build` 读值、读个数、递归 `个数` 次，结构和编码一一对应，读起来就是编码的定义。题目的树高可达 `1000`，递归深度会撞上 Python 上限，所以递归版要加 `sys.setrecursionlimit` 或改迭代。

**解法三：层序 + `null` 分隔**（题面给的格式）：BFS，每个结点的孩子写完后写一个 `null`。解码用队列，按顺序给队首结点分配孩子，不会递归，深度无关；缺点是 `null` 让输出更长，需要区分「值」与「空标记」。

**怎么选。** 面试里先写递归版（`10` 行，讲清编码思想），然后主动说「高 1000 会爆栈」并给出显式栈版本，是最稳的路径；要和 LeetCode 的输入格式互转时用层序版。
