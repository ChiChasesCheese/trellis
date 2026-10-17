"""有三个 bug 的 install_order，代码评审练习用。

读它、找出 bug、写出能暴露每个 bug 的最小输入，再对照题解。
"""
from collections import defaultdict, deque


def install_order(deps):
    indegree = {n: len(ds) for n, ds in deps.items()}
    dependents = defaultdict(set)
    for node, ds in deps.items():
        for d in set(ds):
            dependents[d].add(node)

    queue = deque(n for n, c in indegree.items() if c == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in dependents[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order
