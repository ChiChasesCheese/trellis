---
id: uth-ai-dedup-3-union-find
node: ai.dedup
type: qa
step: 3
---
## Q
**A≈B、B≈C 怎么办**｜datatrove · 0.8.0 MinHash

配出来一堆重复对：A-B、B-C、D-E，最后每组该留哪一篇？

## A
**背景。** 配出的是两两成对，重复却是成组的：A 像 B、B 像 C，三篇只该留一篇。逐对处理很容易漏掉传递关系，因为 A 和 C 并没有直接配上。

**结构。** 并查集（union-find）：每篇文章起初自成一组；读到一对重复，就把两组合并；最后每组有一个「根」。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 182">
<g font-size="12" font-family="sans-serif" text-anchor="middle" fill="currentColor" stroke="currentColor">
<ellipse cx="105" cy="75" rx="95" ry="52" style="fill:none;stroke-width:1;stroke-dasharray:4,3"/>
<ellipse cx="270" cy="75" rx="60" ry="52" style="fill:none;stroke-width:1;stroke-dasharray:4,3"/>
<line x1="53" y1="75" x2="92" y2="75" style="stroke-width:1"/>
<line x1="118" y1="75" x2="157" y2="75" style="stroke-width:1"/>
<line x1="263" y1="75" x2="277" y2="75" style="stroke-width:1"/>
<circle cx="40" cy="75" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1;stroke-dasharray:4,3"/>
<text x="40" y="79.2" stroke="none">A</text>
<circle cx="105" cy="75" r="13" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4);stroke-width:2"/>
<text x="105" y="79.2" style="stroke:none;fill:#fff">B</text>
<circle cx="170" cy="75" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1;stroke-dasharray:4,3"/>
<text x="170" y="79.2" stroke="none">C</text>
<circle cx="250" cy="75" r="13" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4);stroke-width:2"/>
<text x="250" y="79.2" style="stroke:none;fill:#fff">D</text>
<circle cx="290" cy="75" r="13" style="fill:var(--chip,rgba(59,111,212,0.12));stroke-width:1;stroke-dasharray:4,3"/>
<text x="290" y="79.2" stroke="none">E</text>
<text x="105" y="14" style="stroke:none;fill:var(--dim,#6b7280)">簇1</text>
<text x="270" y="14" style="stroke:none;fill:var(--dim,#6b7280)">簇2</text>
<text x="105" y="118" style="stroke:none;fill:var(--dim,#6b7280)">A与C不一定像</text>
<text x="170" y="150" stroke="none">查到的重复对: A-B, B-C, D-E</text>
<text x="170" y="170" style="stroke:none;fill:var(--dim,#6b7280)">实心=留下(根), 虚线=删除</text>
</g>
</svg>
```

**细节。**

- datatrove 的聚类阶段用路径压缩（path compression）加按大小合并（union by size），操作近似常数时间
- 每组只留根，其余文章写进 `.remove` 文件，最后一步据此过滤
- 这一步只能单进程跑，因为所有重复对要进同一个并查集

**坑。** 传递会把「不太像」的也连进来：A≈B、B≈C 但 A 与 C 可能不像，仍然成一簇，一簇只留一篇，可能多删。

**例题：** LC 721 账户合并（同样是两两「相同」的关系，合并成组）

每个账户是名字加若干邮箱，两个账户有共同邮箱就属于同一个人；合并后每人一个账户，邮箱按字典序排好。例：两个 `John` 共享 `johnsmith@mail.com`，合成一个，另一个 `John` 不变。

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
