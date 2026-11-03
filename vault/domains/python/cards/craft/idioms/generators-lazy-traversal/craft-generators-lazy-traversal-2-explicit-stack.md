---
id: craft-generators-lazy-traversal-2-explicit-stack
node: craft.idioms.generators-lazy-traversal
type: qa
step: 2
---
## Q
**生成器与惰性遍历 · 遍历树为什么用显式栈加 `yield`，而不是递归的 `yield from`**｜写法

递归写法最直观：`yield n`，然后对每个子节点 `yield from rec(child)`。`find` 的目录遍历却用了一个显式的栈和 `while` 循环。深目录下递归写法会怎样？逆序压栈又是为了什么？

## A
**要点。** 递归生成器里每一层 `yield from` 都是一层嵌套的生成器调用，深度受 Python 的递归上限约束（默认 1000）：目录足够深就抛 `RecursionError`；而且每个值要穿过所有嵌套的层才到达调用方，深度越大每次取值越慢。显式栈把「还没处理的节点」放在一个列表里，深度只受内存限制，每个 `yield` 都是 O(1)。栈是后进先出，要让同层按名字**升序**弹出，就得按**降序**压入，即 `sorted(..., reverse=True)`。

```python
@dataclass
class Node:
    name: str
    children: dict[str, "Node"] = field(default_factory=dict)

def chain(depth: int) -> Node:                    # 一条很深的目录链 /d/d/d/...
    root = cur = Node("/")
    for _ in range(depth):
        nxt = Node("d"); cur.children["d"] = nxt; cur = nxt
    return root

def rec(n: Node) -> Iterator[Node]:               # 递归生成器: yield from 每层多一层调用栈
    yield n
    for name in sorted(n.children):
        yield from rec(n.children[name])

def explicit(root: Node, prune=lambda n: False) -> Iterator[Node]:
    stack = [root]
    while stack:
        n = stack.pop()
        yield n
        if prune(n):
            continue                              # 剪枝: 不展开, 子树的节点根本不会入栈
        for name in sorted(n.children, reverse=True):   # 逆序压栈 -> 弹出时是升序
            stack.append(n.children[name])

deep = chain(5000)
try:
    sum(1 for _ in rec(deep))
except RecursionError:
    print("递归生成器 深度 5000: RecursionError")
print("显式栈     深度 5000:", sum(1 for _ in explicit(deep)), "个节点")

tree = Node("/", {"b": Node("b", {"x": Node("x")}), "a": Node("a", {"y": Node("y")}), "c": Node("c")})
print("前序、同层按名字升序:", [n.name for n in explicit(tree)])
print("剪掉 a 之后:", [n.name for n in explicit(tree, prune=lambda n: n.name == "a")])
```

实际输出：

```
递归生成器 深度 5000: RecursionError
显式栈     深度 5000: 5001 个节点
前序、同层按名字升序: ['/', 'a', 'y', 'b', 'x', 'c']
剪掉 a 之后: ['/', 'a', 'b', 'x', 'c']
```

**为什么还有一个好处。** 显式栈让剪枝很自然：判定要不要展开某个目录，是「是否把它的子节点压栈」这一个 `if`，被剪掉的子树的节点根本不会被创建；递归生成器里想做到同样的事，要么靠调用方协作，要么靠额外的参数。

**易错。** 栈里存的不只是节点：目录符号链接可能形成环，`find` 把「祖先目录链」和节点一起压栈，用来检测环。显式栈让你有地方放遍历过程中要带的上下文（深度、祖先、路径）。
