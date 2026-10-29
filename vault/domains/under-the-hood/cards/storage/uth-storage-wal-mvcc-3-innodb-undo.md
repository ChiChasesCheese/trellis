---
id: uth-storage-wal-mvcc-3-innodb-undo
node: storage.wal-mvcc
type: qa
step: 4
---
## Q
**InnoDB：原地更新，旧版本放 undo 链**｜InnoDB · MySQL 8.4

InnoDB 同样是 MVCC，旧版本放在哪？一致性读（consistent read）怎样读到它们？

## A
**背景。** 和 PostgreSQL 相反，InnoDB 不想让表里堆满旧版本。

**结构。** 聚簇索引里的行永远是最新版本，每行多 6 字节 `DB_TRX_ID`（最后改它的事务）和 7 字节 `DB_ROLL_PTR`（指向 undo 记录的指针）。旧版本放在回滚段的 undo 记录里，串成一条链。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 126">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">聚簇索引行 (最新)</text>
<rect x="8" y="22" width="118" height="68" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="67" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最新版本</text>
<text x="67" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">DB_TRX_ID</text>
<text x="67" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">DB_ROLL_PTR</text>
<text x="150" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回滚段 undo 链</text>
<line x1="126" y1="76" x2="142.938" y2="65.2213" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="148,62 144.5,67.8 141.3,62.7" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<rect x="148" y="36" width="84" height="52" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="190" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">undo</text>
<text x="190" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧版本 1</text>
<line x1="232" y1="62" x2="244" y2="62" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,62 244.0,65.0 244.0,59.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<rect x="250" y="36" width="82" height="52" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="291" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">undo</text>
<text x="291" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧版本 2</text>
<text x="170" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按读视图往回走, 直到版本可见</text>
</svg>
```

**细节。**

- 读事务按读视图（相当于快照）沿 `DB_ROLL_PTR` 往回走，直到找到可见的版本。
- 删除也是更新：先打删除标记，没有快照需要时由 purge 线程真正移除。

**坑。** 长事务让 undo 越积越多；官方建议定期提交，连只读事务也一样。

**为什么。** PostgreSQL 新旧版本都在表里（要 VACUUM）；InnoDB 表里只留最新版本，代价是读旧版本要回溯。

**对应 LeetCode：** 无直接对应的题
