---
id: tlc-patterns-union-find-4-accounts
node: patterns.union-find
type: qa
step: 4
---
## Q
**并查集（Union-Find）｜账户合并（LC 721）：非整数节点怎么用并查集**

多个账户共享邮箱就属于同一个人，要把账户合并。节点是什么？合并哪些点？怎么输出？

## A
把**邮箱**当节点；同一账户里的所有邮箱互相连通。非整数节点先用字典映射成编号，再建并查集；最后按根分组、排序输出。

```python
from collections import defaultdict
class UnionFind:
    def __init__(self, n: int) -> None:
        self.p = list(range(n))
    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]      # 路径减半：每走一步顺便缩短一层
            x = self.p[x]
        return x
    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        self.p[ra] = rb
        return ra != rb

def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    email_id: dict[str, int] = {}
    owner: dict[str, str] = {}
    for acc in accounts:
        for e in acc[1:]:
            if e not in email_id:
                email_id[e] = len(email_id)
                owner[e] = acc[0]
    uf = UnionFind(len(email_id))
    for acc in accounts:
        first = email_id[acc[1]]
        for e in acc[2:]:
            uf.union(first, email_id[e])       # 同一账户里的邮箱全部合并到第一个
    groups: defaultdict[int, list[str]] = defaultdict(list)
    for e, i in email_id.items():
        groups[uf.find(i)].append(e)
    return [[owner[es[0]], *sorted(es)] for es in groups.values()]
```

输入 `[["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]`：三个 `John` 邮箱合并成一组 `['John','john00@mail.com','john_newyork@mail.com','johnsmith@mail.com']`，另有 `['John','johnnybravo@mail.com']` 与 `['Mary','mary@mail.com']`。

- 这个精简版用"路径减半"压缩路径，不做按大小合并，仍是近似 `O(1)`。
- 传递性是关键：账户 A、B 共享邮箱 1，B、C 共享邮箱 2，则三者合并；并查集自动处理。
- 时间 `O(N α(N) + N log N)`（`N` 为邮箱总数，排序是 `log`）。
