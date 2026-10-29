---
id: tlc-accounts-merge-4-followup
node: a.accounts-merge
type: qa
step: 4
---
## Q
**LC 721 账户合并**｜追问

面试官接着问：（1）不用并查集，用图搜索怎么做？（2）账户一个个地陆续到达，随时要查「这个邮箱属于哪个人」？（3）数据大到单机放不下？

## A
1. **图 DFS**：邮箱作结点，同一账户里的邮箱连边（以账户的第一个邮箱为中心，连成星形即可保持连通），每个连通分量就是一个人；用栈遍历，收集邮箱，排序，名称取分量里任意一个邮箱对应的账户名：

```python
from collections import defaultdict


def accounts_merge_graph(accounts: list[list[str]]) -> list[list[str]]:
    graph: defaultdict[str, set[str]] = defaultdict(set)    # 邮箱 -> 同一账户里的其他邮箱
    name_of: dict[str, str] = {}
    for name, *emails in accounts:
        for email in emails:
            name_of[email] = name
            graph[emails[0]].add(email)                     # 以账户第一个邮箱为中心连边
            graph[email].add(emails[0])
    seen: set[str] = set()
    result: list[list[str]] = []
    for start in graph:
        if start in seen:
            continue
        seen.add(start)
        stack, component = [start], []
        while stack:
            email = stack.pop()
            component.append(email)
            for nxt in graph[email] - seen:
                seen.add(nxt)
                stack.append(nxt)
        result.append([name_of[start], *sorted(component)])
    return result
```

2. **在线**：并查集天然支持增量。新账户来了，对它的每个邮箱做一次 `owner` 查找和 `union`；查询邮箱的主人用 `find(owner[email])`，再取该根账户的名称。若要支持“拆分”（账户被删除），并查集不行，需要别的结构。
3. **分布式**：按邮箱的哈希分片，每个分片内部先合并；跨分片的账户（同一个账户的邮箱落在多个分片）再通过一轮“集合 id 合并”把分片结果连起来，类似分布式连通分量标记。

**Python 提醒**：`for name, *emails in accounts` 用星号解包把名称和邮箱分开；`graph[email] - seen` 是集合差，会生成新集合，所以可以在循环里放心修改 `seen`。
