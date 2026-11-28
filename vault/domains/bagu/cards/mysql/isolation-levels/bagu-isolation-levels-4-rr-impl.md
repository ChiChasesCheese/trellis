---
id: bagu-isolation-levels-4-rr-impl
node: a.mysql.isolation-levels
type: qa
step: 4
---
## Q
**RR 的实现 · MVCC 和锁各负责什么，还有幻读吗**｜追问

面试官：「InnoDB 的 RR 怎么实现？你说它能防幻读，是完全没有幻读了吗？」

## A
**基本回答。** InnoDB 的 RR 是两套机制分工：快照读（普通 `SELECT`）靠 MVCC，读的是事务第一次读时固定下来的一致性快照，不加锁；当前读（`FOR UPDATE`、`FOR SHARE`、`UPDATE`、`DELETE`、`INSERT`）读最新数据，靠行锁和 next-key 锁阻止别人往范围里插入。但不是完全没有幻读：先快照读，再对别的事务刚提交的新行做 `UPDATE`，当前读看得到这一行，并把行的事务版本改成自己的，之后快照读就能看到它了。
演示（8.0.46）：A `COUNT` 得 3，B 插入 id=7 并提交，A 再 `COUNT` 仍是 3，A `UPDATE ... WHERE id=7` 命中 1 行，再 `COUNT` 变成 4。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事务 A</text>
<text x="176" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事务 B</text>
<rect x="8" y="22" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="39.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">COUNT → 3（建视图）</text>
<rect x="176" y="56" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="254.0" y="73.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INSERT id=7 并提交</text>
<rect x="8" y="90" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86.0" y="107.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">COUNT → 3（快照读）</text>
<rect x="8" y="124" width="156" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86.0" y="141.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">UPDATE id=7 命中 1 行</text>
<rect x="8" y="158" width="156" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86.0" y="175.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">COUNT → 4（幻读）</text>
<line x1="86" y1="48" x2="86.0" y2="83.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,90.0 82.8,83.0 89.2,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="86" y1="116" x2="86.0" y2="117.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,124.0 82.8,117.0 89.2,117.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="86" y1="150" x2="86.0" y2="151.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,158.0 82.8,151.0 89.2,151.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="176" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">快照读看不到 id=7</text>
<text x="176" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">当前读看得到，并把</text>
<text x="176" y="156" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">行版本改成 A 自己的</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">彻底防住：对范围 FOR UPDATE（next-key 锁）</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">或用唯一约束兜底，重复插入直接报错</text>
</svg>
左列是事务 A 的步骤，右边是事务 B 插入。A 的前两次 `COUNT` 都是 3（快照读看不到 id=7）；当 A 用 `UPDATE` 这个当前读命中 id=7 后，这一行的版本变成 A 自己的，再 `COUNT` 就变成 4。
**举个例子。** 抢红包，要求每个用户只能领一次：
1. **先查：** 两个并发请求都执行 `SELECT COUNT(*)`（快照读）判断用户是否领过，都读到 0。
2. **都认为没领过：** 两边各自执行 `INSERT`。
3. **结果：** 用户领了两次，因为判断和插入之间，快照读看不到对方的插入。
4. **提高隔离级别没用：** RR 的快照读本来就看不到别人新插入的行，问题不在隔离级别。
5. **解决：** 给 `(activity_id, user_id)` 建唯一键，第二个插入失败；对范围 `SELECT ... FOR UPDATE` 也能防重复，但两个请求不会排队：记录不存在时它们都能拿到同一段间隙锁（间隙锁之间不冲突），接着各自插入时互相等对方的间隙锁，形成死锁，InnoDB 回滚其中一个。所以首选唯一键。
**容易错。**
- **以为 RR 完全没有幻读：** 快照读没有，混用当前读会有。
- **以为提高隔离级别能解决先查后插：** 要靠唯一约束或范围加锁。
- **以为 UPDATE 读到的和 SELECT 一样：** `UPDATE` 是当前读，读的是最新数据，可以命中快照里看不到的新行。
- **忘了自己改过的行对自己总是可见：** 所以当前读改过之后，快照读也能看到它。
