---
id: uth-python-mutability-args-3-shallow-deep
node: python.mutability-args
type: qa
step: 3
---
## Q
**拷贝嵌套列表，内层会跟着变吗**｜Python · CPython 3.14

`b = a.copy()` 之后改 `b[0].append(9)`，为什么 `a` 里也出现了 9？`copy.deepcopy` 又是怎么避免的？

## A
**背景。** `b = a` 根本没复制，只是多了个名字。要独立副本就得新造对象。可容器里装的也是指针，复制到哪一层，必须选一个。

**结构。** 浅拷贝（shallow copy）新建外层容器，里面装着和原来相同的元素指针，元素本身不复制：`a.copy()`、`a[:]`、`list(a)`、`copy.copy(a)` 都是。深拷贝（deep copy）则递归复制每一层。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 245">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a = [[0]]</text>
<text x="120" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">b = a.copy()  浅拷贝</text>
<rect x="10" y="28" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="24" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="10" y="74" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="24" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="90" y="28" width="34" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="107" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<rect x="90" y="74" width="34" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="107" y="89" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<rect x="210" y="50" width="50" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="235" y="67" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[0]</text>
<line x1="38" y1="39" x2="88" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="88.0,39.0 82.0,42.0 82.0,36.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="38" y1="85" x2="88" y2="85" stroke-width="1.2" stroke="currentColor"/>
<polygon points="88.0,85.0 82.0,88.0 82.0,82.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="124" y1="39" x2="208" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,58.0 201.5,59.6 202.8,53.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="124" y1="85" x2="208" y2="68" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,68.0 202.7,72.1 201.5,66.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="285" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">共享</text>
<text x="285" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">内层</text>
<line x1="10" y1="124" x2="330" y2="124" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="120" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">b = deepcopy(a)  深拷贝</text>
<rect x="10" y="156" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="24" y="171" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="10" y="202" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="24" y="217" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="90" y="156" width="34" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="107" y="171" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<rect x="90" y="202" width="34" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="107" y="217" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">•</text>
<rect x="210" y="154" width="50" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="235" y="171" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[0]</text>
<rect x="210" y="200" width="50" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="235" y="217" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[0]</text>
<line x1="38" y1="167" x2="88" y2="167" stroke-width="1.2" stroke="currentColor"/>
<polygon points="88.0,167.0 82.0,170.0 82.0,164.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="38" y1="213" x2="88" y2="213" stroke-width="1.2" stroke="currentColor"/>
<polygon points="88.0,213.0 82.0,216.0 82.0,210.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="124" y1="167" x2="208" y2="167" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,167.0 202.0,170.0 202.0,164.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="124" y1="213" x2="208" y2="213" stroke-width="1.2" stroke="currentColor"/>
<polygon points="208.0,213.0 202.0,216.0 202.0,210.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="285" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">各一份</text>
</svg>
```

**细节。**

- `deepcopy` 用一个 `memo` 字典记着「原对象的 id → 新对象」。
- 同一个对象被引用两次，只复制一次，副本里仍然共享；两个对象互相指着（有环）也不会无限递归。
- 复制列表时，先把新列表登记进 `memo`，再逐个复制元素。
- `int`、`str`、`None` 这类不可变的原子类型直接返回自身，不复制。

**为什么。** 默认只复制外层：复制整张对象图又慢又占内存，需要时再显式深拷贝。

**例题：** LC 133 克隆图

给无向连通图中一个节点的引用，返回整张图的深拷贝（所有节点都是新建的）。每个节点有整数 `val` 和邻居列表 `neighbors`，节点数 `<= 100`。

```python
def clone_graph(node: Node | None) -> Node | None:
    copies: dict[Node, Node] = {}              # 原节点 -> 它的拷贝，同时充当 visited

    def dfs(cur: Node) -> Node:
        if cur in copies:
            return copies[cur]                 # 已经克隆过：直接复用，环到这里就断了
        copies[cur] = clone = Node(cur.val)    # 先登记再递归邻居，遇到环才不会死循环
        clone.neighbors = [dfs(nb) for nb in cur.neighbors]
        return clone

    return dfs(node) if node else None
```
