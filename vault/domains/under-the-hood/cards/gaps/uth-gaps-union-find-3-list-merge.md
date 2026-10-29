---
id: uth-gaps-union-find-3-list-merge
node: gaps.union-find
type: qa
step: 3
---
## Q
**PostgreSQL 的“并查集”其实是链表**｜PostgreSQL · 17

等价类的合并正是并查集问题。PostgreSQL 的源码里真的有父指针和路径压缩吗？

## A
**结构。** 没有。每个等价类就是一个成员链表，合并时把一个类的链表接到另一个后面（`list_concat`），再把被并的类从类列表里摘掉。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 188">
<text x="14" y="38" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">ec1</text>
<rect x="44" y="22" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="71" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a.x</text>
<rect x="102" y="22" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="129" y="38" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b.y</text>
<text x="14" y="80" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">ec2</text>
<rect x="44" y="64" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="71" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c.z</text>
<rect x="102" y="64" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="129" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<line x1="100" y1="90" x2="100" y2="116" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M100,122 L97,116 L103,116 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<text x="108" y="110" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">list_concat</text>
<text x="14" y="144" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">ec1</text>
<rect x="44" y="124" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="71" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a.x</text>
<rect x="102" y="124" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="129" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b.y</text>
<rect x="160" y="124" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="187" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c.z</text>
<rect x="218" y="124" width="54" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="245" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">5</text>
<rect x="266" y="64" width="62" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--dim,#6b7280)"/>
<text x="297" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">ec2</text>
<line x1="296" y1="90" x2="266.4" y2="117.9" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<path d="M262,122 L264.3,115.7 L268.4,120.1 Z" stroke="none" style="fill:var(--dim,#6b7280)"/>
<text x="268" y="108" text-anchor="end" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">ec_merged</text>
<text x="170" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">类 ec2 留下指向 ec1 的指针 别处的旧引用仍能找到它</text>
</svg>
```

**细节。**

- 被并掉的类不能直接丢，别处（例如排序键）还拿着它的指针：它留下 `ec_merged`，指向并入的那个类
- 源码注释写明：这是标准的并查集问题，有比链表更好的数据结构，成为瓶颈再加速，「但现在，简单就是美」
- 合并只发生在规划开头；等价类定型（`ec_merging_done`）之后再合并会直接报错

**为什么。** 一条查询里的相等条件通常很少，链表拼接足够快；并查集要在元素很多时才划算。

**例题：** LC 721 账户合并（同类：LC 547 省份数量）

`accounts[i]` 的第一个元素是名字，其余是邮箱。两个账户只要有共同邮箱就属于同一个人（同名也可能是不同的人）。合并后返回：名字加按 ASCII 排序的邮箱。`1 <= accounts.length <= 1000`。

```python
from collections import defaultdict


def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    parent = list(range(len(accounts)))        # 并查集：以账户下标为结点

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]      # 路径折半
            x = parent[x]
        return x

    owner: dict[str, int] = {}                 # 邮箱 -> 第一个出现它的账户
    for i, (_, *emails) in enumerate(accounts):
        for email in emails:
            j = owner.setdefault(email, i)
            if j != i:                         # 邮箱已属于别的账户：两个账户合并
                parent[find(i)] = find(j)

    groups: defaultdict[int, list[str]] = defaultdict(list)
    for email, i in owner.items():
        groups[find(i)].append(email)
    return [[accounts[root][0], *sorted(emails)] for root, emails in groups.items()]
```
