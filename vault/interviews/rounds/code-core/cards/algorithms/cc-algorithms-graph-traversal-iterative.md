---
id: cc-algorithms-graph-traversal-iterative
node: algorithms.graph-traversal
type: qa
---
## Q
A dependency chain of 5·10^4 nodes makes your recursive DFS raise `RecursionError`. Two fixes — which one, and why not the other?

## A
**Rewrite it iteratively with an explicit stack.** That is the only version that scales.

```python
stack = [start]
while stack:
    u = stack.pop()
    for v in adj[u]:
        if v not in seen:
            seen.add(v); stack.append(v)
```

- Python's default limit is 1000 frames; a chain that long is exactly what a hidden performance test builds.
- `sys.setrecursionlimit(300000)` is a trap: it moves the failure from a clean exception to a C-stack crash, and the grader shows you nothing at all.
- For **post-order** work (topological order, tree DP, "process a node after its children"), push `(node, state)` pairs and act on a node the second time you see it.
- The stack version visits neighbours in reverse order compared to recursion; if the traversal order is graded, push the neighbour list reversed.

## Q zh
一条 5·10^4 个节点的依赖链让你的递归 DFS 抛出 `RecursionError`。有两种修法 —— 选哪个，为什么不选另一个？

## A zh
**用显式栈改写成迭代版。** 只有这个版本能扩展。

```python
stack = [start]
while stack:
    u = stack.pop()
    for v in adj[u]:
        if v not in seen:
            seen.add(v); stack.append(v)
```

- Python 默认限制是 1000 层；构造这么长的链正是隐藏性能测试要做的事。
- `sys.setrecursionlimit(300000)` 是个陷阱：它把干净的异常变成 C 栈崩溃，而 grader 什么都不会显示给你。
- 需要**后序**处理时（拓扑序、树形 DP、「在子节点之后处理该节点」），把 `(node, state)` 成对入栈，在第二次见到该节点时才处理它。
- 与递归相比，栈版本访问邻居的顺序是相反的；如果遍历顺序会被判分，就把邻居列表反过来再入栈。
