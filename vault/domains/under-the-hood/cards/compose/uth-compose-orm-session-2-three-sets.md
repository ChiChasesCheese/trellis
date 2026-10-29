---
id: uth-compose-orm-session-2-three-sets
node: compose.orm-session
type: qa
step: 2
---
## Q
**身份映射 + 三个待办集合**｜SQLAlchemy · 2.0.55

Session 内部用哪几个结构来满足这些要求？它们怎样互相指向？

## A
**结构。** 一张身份映射（identity map）：`(类, 主键) → 对象`，保证同一行只有一个对象。再加三个集合记账：`new`（待 INSERT）、`dirty`（已加载且被改过，待 UPDATE）、`deleted`（待 DELETE）。集合里放的就是身份映射里的那些对象本身，不是拷贝。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 252">
<rect x="8" y="24" width="150" height="92" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="83" y="40" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">identity map</text>
<rect x="18.0" y="50" width="130" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="83" y="66.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">(User,5) -&gt; u5</text>
<rect x="18.0" y="82" width="130" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="83" y="98.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">(User,7) -&gt; u7</text>
<rect x="202.0" y="24" width="120" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="4 3"/>
<text x="262" y="40.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">new: u9 (无主键)</text>
<rect x="202.0" y="56" width="120" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="262" y="72.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">dirty: u5</text>
<rect x="202.0" y="88" width="120" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="262" y="104.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">deleted: u7</text>
<line x1="202" y1="68" x2="155.0" y2="62.8" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="148,62 154.6,66.0 155.3,59.6" style="fill:var(--accent,#3b6fd4)"/>
<line x1="202" y1="100" x2="155.0" y2="94.8" stroke="currentColor" stroke-width="1"/>
<polygon points="148,94 154.6,98.0 155.3,91.6" fill="currentColor"/>
<line x1="322" y1="36" x2="332" y2="36" stroke="currentColor" stroke-width="1"/>
<line x1="322" y1="68" x2="332" y2="68" stroke="currentColor" stroke-width="1"/>
<line x1="322" y1="100" x2="332" y2="100" stroke="currentColor" stroke-width="1"/>
<line x1="332" y1="36" x2="332" y2="146" stroke="currentColor" stroke-width="1"/>
<line x1="332" y1="146" x2="170" y2="146" stroke="currentColor" stroke-width="1"/>
<line x1="170" y1="146" x2="170.0" y2="157.0" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="170,164 173.2,157.0 166.8,157.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="95.0" y="164" width="150" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="170" y="181.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">flush()</text>
<text x="170" y="208" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1 INSERT   2 UPDATE   3 DELETE</text>
<line x1="170" y1="214" x2="170.0" y2="221.0" stroke="currentColor" stroke-width="1"/>
<polygon points="170,228 173.2,221.0 166.8,221.0" fill="currentColor"/>
<rect x="140.0" y="228" width="60" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1"/>
<text x="170" y="242.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">DB</text>
</svg>
```

| 操作 | 碰哪几个结构 | 复杂度 |
|---|---|---|
| `get(User, 5)` | 身份映射查键，命中直接返回；没有才查库并登记 | O(1) |
| `add(obj)` | 加入 `new` | O(1) |
| `obj.name = "x"` | 对象被标记为已修改，进 `dirty` | O(1) |
| `delete(obj)` | 加入 `deleted` | O(1) |
| `flush()` | 读三个集合发 SQL；成功后清空它们，新对象进身份映射 | O(改动个数) |

**例题：** LC 133 克隆图

给无向连通图中一个节点的引用，返回整张图的深拷贝（所有节点都新建）。每个节点有整数 `val` 和邻居列表 `neighbors`，节点数不超过 100。例：邻接表 `[[2,4],[1,3],[2,4],[1,3]]` 克隆后结构相同，所有节点都是新对象。`copies: 原节点 → 拷贝` 就是身份映射：同一个原节点永远只对应一个拷贝。

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
