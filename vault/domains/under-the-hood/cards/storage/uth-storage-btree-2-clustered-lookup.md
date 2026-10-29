---
id: uth-storage-btree-2-clustered-lookup
node: storage.btree
type: qa
step: 2
---
## Q
**聚簇索引与回表**｜InnoDB · MySQL 8.4

InnoDB 按二级索引（比如 `name`）查整行要走几棵 B+ 树？为什么主键不宜太长？

## A
**背景。** 一张表可以有多个索引（按主键找、按 `name` 找），每个索引都是一棵 B+ 树。如果每棵树的叶子都存整行，同一行就存了很多份。

**结构。** 聚簇索引（clustered index）就是按主键组织的 B+ 树，叶子页存整行。二级索引的叶子只存“二级键 + 主键值”。按 `name` 查整行：先在二级索引找到主键，再到聚簇索引按主键查一次，这一步叫回表，共 2 次树查找。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 148">
<text x="73" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">二级索引 (name)</text>
<text x="267" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">聚簇索引 (主键)</text>
<polygon points="73,24 8,84 138,84" fill="none" stroke="currentColor" stroke-width="1.2"/>
<polygon points="267,24 202,84 332,84" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="8" y="84" width="130" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="73" y="100.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Bob  42</text>
<rect x="202" y="84" width="130" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="267" y="100.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">42  整行</text>
<line x1="138" y1="100" x2="196" y2="100" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="202,100 196.0,103.0 196.0,97.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="92" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">回表</text>
<text x="170" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">找 1 行要查 2 棵 B+ 树</text>
</svg>
```

**细节。**

- 索引已含所需全部列（覆盖索引）时，不用回表。
- 没有主键也没有合适的唯一索引时，InnoDB 生成隐藏的 6 字节行号作聚簇键。

**为什么。** 整行只存一份；代价是每条二级索引记录都带一份主键，主键越长，所有二级索引越大。

**对应 LeetCode：** 无直接对应的题
