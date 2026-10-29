---
id: uth-gaps-tree-dfs-3-hardlink
node: gaps.tree-dfs
type: qa
step: 3
---
## Q
**同一个文件有两个名字，du 只数一次**｜GNU coreutils · du 9.12

备份目录里很多文件是指向同一份数据的硬链接（hard link）。`du` 为什么不会把它们数成两份？

## A
**背景。** 文件名只是目录里的一条记录，指向一个 inode（存着文件元数据和数据块位置的结构）。硬链接就是多个名字指向同一个 inode，数据只有一份。走到一个名字就数一次，同一份数据会被数好几遍。

**结构。** 树里出现了「多条路通到同一个点」，其实是图。`du` 对每个 `st_nlink > 1`（有多个名字）的非目录文件，把（设备号，inode 号）放进哈希集合：已在集合里就跳过，否则数它并记下。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<rect x="10" y="30" width="106" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">/data/a.iso</text>
<rect x="10" y="90" width="106" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">/backup/a.iso</text>
<line x1="116" y1="44" x2="144.8" y2="61" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M150,64 L143.3,63.5 L146.3,58.4 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<line x1="116" y1="102" x2="144.8" y2="85" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<path d="M150,82 L146.3,87.6 L143.3,82.5 Z" stroke="none" style="fill:var(--dim,#6b7280)"/>
<rect x="150" y="48" width="84" height="50" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="192" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">inode 7</text>
<text x="192" y="88" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">链接数 2</text>
<line x1="234" y1="73" x2="256" y2="73" fill="none" stroke="currentColor" stroke-width="1.2"/>
<path d="M262,73 L256,76 L256,70 Z" fill="currentColor" stroke="none"/>
<rect x="262" y="61" width="66" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="295" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">数据块</text>
<rect x="60" y="128" width="220" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="170" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">{ (设备, 7) }</text>
<text x="170" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">已数过的集合</text>
<text x="14" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">第 1 个名字 数一次 并记入集合</text>
<text x="14" y="198" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">第 2 个名字 已在集合里 跳过</text>
</svg>
```

**细节。**

- 只有一个名字的文件通常不进集合，省内存
- `du -l`（`--count-links`）关掉去重，每个名字都数

**坑。** 用硬链接做的快照目录（`cp -al`），`du` 一次扫多个快照时，共享的数据只算在最先扫到的那个里，后面的看起来几乎是空的。

**例题：** LC 133 克隆图

给无向连通图中一个结点的引用，返回整张图的深拷贝（所有结点都是新建的）。每个结点有 `val` 和邻居列表 `neighbors`。结点数 `[0, 100]`。字典 `copies` 既存拷贝，又当 visited 用，图里绕回来的边不会被拷贝两次。

```python
from collections import deque

def clone_graph(node: Node | None) -> Node | None:
    if node is None:
        return None
    copies = {node: Node(node.val)}            # 原节点 -> 它的拷贝，同时充当 visited
    queue = deque([node])
    while queue:
        cur = queue.popleft()
        for nb in cur.neighbors:
            if nb not in copies:               # 第一次见到：先建拷贝再入队
                copies[nb] = Node(nb.val)
                queue.append(nb)
            copies[cur].neighbors.append(copies[nb])
    return copies[node]
```
