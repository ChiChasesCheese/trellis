---
id: amz-dag-runner-stage1-kahn-in-code
node: amazon.amz-dag-runner
type: qa
step: 3
tags: [grown]
---
## Q
在 Amazon DAG 执行器的第 1 关，用 Python 写出 Kahn 算法（入度为 0 的节点反复出队）的 install_order，deps[x] 是 x 的前置依赖。

## A
只出现在依赖里的名字也要登记，入度按去重后的集合算，排完要核对数量：

```python
def install_order(deps):
    need = {n: set(ds) for n, ds in deps.items()}
    users = {}
    for n, ds in list(need.items()):
        for d in ds:
            need.setdefault(d, set())
            users.setdefault(d, []).append(n)
    left = {n: len(ds) for n, ds in need.items()}
    ready = [n for n, c in left.items() if c == 0]
    for n in ready:  # 遍历中追加：列表迭代会看到新元素
        for u in users.get(n, ()):
            left[u] -= 1
            if left[u] == 0: ready.append(u)
    if len(ready) != len(need): raise ValueError("cycle")
    return ready
```

例：{"a": ["b"]} 返回 ["b", "a"]；时间 O(V+E)。
