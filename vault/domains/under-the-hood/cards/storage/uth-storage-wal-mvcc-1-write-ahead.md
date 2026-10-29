---
id: uth-storage-wal-mvcc-1-write-ahead
node: storage.wal-mvcc
type: qa
step: 1
---
## Q
**WAL：先写日志，再改数据页**｜SQLite · 3.53 / PostgreSQL · 18

数据库提交事务时，只把日志落盘，数据页稍后再写。崩溃之后靠什么恢复？

## A
**背景。** 提交事务必须保证“断电也不丢”。最直接的办法是把改过的数据页立刻写回磁盘，但数据页散落在文件各处，是随机写，很慢；页写到一半断电，文件还可能损坏。

**结构。** 预写日志（WAL，write-ahead log）：先把“改了什么”按顺序追加到一个日志文件，提交就是追加一条提交记录；数据页留在原处，由检查点（checkpoint）批量写回。崩溃后从最近的检查点开始重放日志，把没写回的改动补上。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 156">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">日志 (顺序追加)</text>
<rect x="8" y="22" width="48" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="32" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改 1</text>
<rect x="60" y="22" width="48" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改 2</text>
<rect x="112" y="22" width="48" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="136" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交</text>
<rect x="164" y="22" width="48" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="188" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改 3</text>
<rect x="216" y="22" width="48" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="240" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改 4</text>
<rect x="268" y="22" width="48" height="24" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="292" y="38.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">提交</text>
<line x1="162" y1="18" x2="162" y2="50" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<text x="176" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">检查点</text>
<line x1="250" y1="48" x2="250" y2="84" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250,90 247.0,84.0 253.0,84.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="260" y="74" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">批量写回</text>
<text x="8" y="82" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数据页</text>
<rect x="8" y="92" width="48" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="32" y="108.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 A</text>
<rect x="60" y="92" width="48" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="108.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 B</text>
<rect x="112" y="92" width="48" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="136" y="108.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 C</text>
<rect x="164" y="92" width="48" height="24" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="188" y="108.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 D</text>
<text x="170" y="148" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">崩溃后: 从检查点起重放日志</text>
</svg>
```

**细节。**

- SQLite 的 WAL 模式：写者只往 WAL 末尾追加；WAL 满 1000 页自动做一次检查点。
- PostgreSQL 的 `checkpoint_timeout` 默认 5 分钟。

**坑。** 页写到一半断电（撕裂页）：PostgreSQL 默认 `full_page_writes = on`，检查点后每页第一次被改，就把整页写进 WAL。

**为什么。** 随机改页变成顺序追加，提交只要一次顺序写。

**对应 LeetCode：** 无直接对应的题
