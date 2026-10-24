---
id: tlc-patterns-topo-sort-4-dfs
node: patterns.topo-sort
type: qa
step: 4
---
## Q
**拓扑排序（Topological Sort）｜DFS 三色法（迭代写法）**

用 DFS 做拓扑排序时，三种状态各表示什么？为什么后序逆序就是拓扑序？链很长时怎样避免递归爆栈？

## A
状态：`0` 未访问；`1` 正在当前递归路径上；`2` 已完成（它的所有后继都处理完）。

- 遇到状态 `1` 的点 ⇒ 沿着当前路径回到了自己 ⇒ **有环**。
- 一个点变成状态 `2` 的那一刻，它的所有后继已经先于它完成并入列表；列表是**后序**，所以把它**逆序**，每个点都排在它的后继之前。

```python
def find_order_dfs(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    graph: list[list[int]] = [[] for _ in range(num_courses)]
    for course, pre in prerequisites:
        graph[pre].append(course)
    state = [0] * num_courses
    post: list[int] = []
    for s in range(num_courses):
        if state[s]:
            continue
        state[s] = 1
        stack = [(s, iter(graph[s]))]      # 显式栈：(节点, 邻居迭代器)，模拟递归
        while stack:
            u, it = stack[-1]
            for v in it:
                if state[v] == 1:
                    return []              # 回到了当前路径上的点：有环
                if state[v] == 0:
                    state[v] = 1
                    stack.append((v, iter(graph[v])))
                    break                  # 先深入 v，回来再继续 u 的剩余邻居
            else:
                state[u] = 2
                post.append(u)
                stack.pop()
    return post[::-1]
print(find_order_dfs(2, [[1, 0]]), find_order_dfs(4, [[1,0],[2,0],[3,1],[3,2]]), find_order_dfs(2, [[0,1],[1,0]]))   # [0, 1] [0, 2, 1, 3] []
```

- `for ... else`：`for` 正常结束（没有 `break`）才执行 `else`，即所有邻居都处理完。
- 2000 门课串成一条链也能正常返回；递归写法在链长超过 1000 时会 `RecursionError`。
- 只用 `visited` 两种状态做不到判环：有向图里"访问过"的点不一定在当前路径上（`a→b, a→c, c→b` 没有环，但 `b` 被访问两次）。
