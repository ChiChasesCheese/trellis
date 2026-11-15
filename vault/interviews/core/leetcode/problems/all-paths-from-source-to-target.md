---
slug: all-paths-from-source-to-target
---
## Q
**LC 797 所有可能的路径**｜Medium

`graph[i]` 是有向无环图中结点 `i` 的所有出邻居（结点 `0` 到 `n-1`）。返回所有从结点 `0` 到结点 `n-1` 的路径，顺序任意。

## A
**一句话。** 回溯 DFS：沿边走一步压入路径，走到终点就收集一份拷贝，回来时弹出；DAG 没有环，不需要 `visited`。

```python
def all_paths_source_target(graph):
    n, res, path = len(graph), [], [0]
    def dfs(u):
        if u == n - 1:
            res.append(path[:])    # 复制一份，别存引用
            return
        for v in graph[u]:
            path.append(v)
            dfs(v)
            path.pop()             # 回溯
    dfs(0)
    return res
```

**复杂度。** 时间 `O(2^n · n)`（路径数最多 `2^(n-2)`，每条拷贝 `O(n)`），空间 `O(n)`（不计结果）。

**易错点。**
- `res.append(path)` 不拷贝：之后 `path` 被修改，所有结果都变成同一个列表。
- 画蛇添足地加 `visited`：一个结点可以出现在不同路径里，标记后会漏路径。

**追问。**
- 图有环怎么办？：路径里要禁止重复结点，回溯时用 `on_path` 集合标记，出栈时清除。
- 只要路径数不要路径本身？：对结点做记忆化 `count(u) = sum(count(v))`，时间 `O(V + E)`。

**同模式。** LC 133 克隆图、LC 207 课程表、LC 113 路径总和 II、LC 79 单词搜索
