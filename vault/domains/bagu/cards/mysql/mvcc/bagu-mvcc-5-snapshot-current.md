---
id: bagu-mvcc-5-snapshot-current
node: a.mysql.mvcc
type: qa
step: 5
---
## Q
**快照读与当前读 · MVCC 能完全防住幻读吗，代价是什么**｜追问

面试官：「什么是快照读和当前读？MVCC 能完全防住幻读吗？代价是什么？」

## A
**基本回答。** 快照读（snapshot read）是普通的 `SELECT`：按 ReadView 去读历史版本，不加锁。当前读（current read）读的是最新版本，并且要加锁，包括 `SELECT ... FOR UPDATE`、`FOR SHARE`、`UPDATE`、`DELETE`、`INSERT`。MVCC 只管快照读：RR 下纯快照读看不到别人后来插入的行，没有幻读；但同一个事务里混用当前读时，当前读看得到最新数据，还会把它改过的行变成「自己的版本」，之后的快照读就能看到这些行，这就是 RR 下仍然可能出现的幻读。要彻底防住，要对范围用当前读加 next-key 锁（行锁加间隙锁）。
扣库存、扣余额这类先判断再修改的操作必须用当前读：读快照会看不到别人刚提交的修改，算出的结果覆盖掉对方，造成丢失更新。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<rect x="8" y="30" width="104" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60.0" y="43.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">快照读</text>
<text x="60.0" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">普通 SELECT</text>
<line x1="112" y1="47" x2="214" y2="47" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="214.0,47.0 207.0,50.2 207.0,43.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="163" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按 ReadView</text>
<text x="163" y="62" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不加锁</text>
<rect x="216" y="30" width="116" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="274.0" y="51.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧版本 余额100</text>
<line x1="274" y1="112" x2="274" y2="66" stroke-width="1.2" stroke="currentColor"/>
<polygon points="274.0,66.0 277.2,73.0 270.8,73.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="282" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">回滚指针</text>
<rect x="8" y="112" width="104" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60.0" y="125.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">当前读</text>
<text x="60.0" y="140.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">改写 / 加锁读</text>
<line x1="112" y1="129" x2="214" y2="129" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="214.0,129.0 207.0,132.2 207.0,125.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="163" y="123" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">读最新</text>
<text x="163" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">并加锁</text>
<rect x="216" y="112" width="116" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="274.0" y="133.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">最新版本 余额200</text>
<text x="8" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">MVCC 只管快照读这条路</text>
<text x="8" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">混用两种读，才会冒出幻读</text>
</svg>
图中第一行是快照读：按 ReadView 找到旧版本，不加锁；第二行是当前读：直接读最新版本，并且要加锁。MVCC 只覆盖快照读这一条路。
**举个例子。**
1. 幻读：A 在 RR 下 `SELECT count(*) FROM orders WHERE user_id=7` → 2（此时建视图）。
2. **B 插入新行：**B 插入一条 `user_id=7` 的订单并提交。
3. **快照读还是 2：**A 再 `SELECT count(*)` → 仍是 2，因为是快照读，看不到 B 的新行。
4. **当前读改到新行：**A 执行 `UPDATE orders SET note='x' WHERE user_id=7`，这是当前读，会改到 3 行，其中 B 新插入的那行的 `trx_id` 变成了 A 自己。
5. **幻读出现：**A 再 `SELECT count(*)` → 3，B 的行突然出现了，这就是幻读。
6. 丢失更新：余额 100，两个请求都用快照读到 100，各自在内存里算出 0 再写回，结果只扣了一次；而 `UPDATE ... SET balance = balance - 100 WHERE balance >= 100` 是当前读，第二个请求读到最新的 0，条件不满足，扣款失败。
7. 代价实测：长事务期间同一行更新 2 万次，`History list length`（还没被清理的 undo 记录数）涨到 2 万。
**容易错。**
- **以为 MVCC 完全防幻读：** 它只管快照读；混用当前读时，仍可能出现幻读，要靠 next-key 锁。
- **以为 RR 下所有读都是快照：** `FOR UPDATE`、`UPDATE` 等都是当前读，读的是最新版本。
- **以为先查后改在 RR 下是安全的：** 快照读到的余额可能已经过期，要让判断和修改发生在同一条当前读语句里，或用乐观锁版本号。
- **忽略长事务：** 一个忘了提交的长事务会让 undo 无法清理，History list length 一直涨。
