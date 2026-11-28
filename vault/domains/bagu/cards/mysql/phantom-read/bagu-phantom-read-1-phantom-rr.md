---
id: bagu-phantom-read-1-phantom-rr
node: b.mysql.phantom-read
type: qa
step: 1
---
## Q
**幻读 · RR 下怎么解决，还有什么特例**｜必会

面试官：「什么是幻读？InnoDB 的可重复读（RR）解决了吗？还有哪些场景会幻读？」

## A
**基本回答。** 幻读是同一事务里，同样条件前后两次查询，结果多出别人新插入的行。InnoDB 的 RR 下：普通读（快照读）靠 MVCC 读事务开始时的快照；加锁读（`SELECT ... FOR UPDATE`、`UPDATE`、`DELETE`，也叫当前读）靠 next-key lock（记录锁加间隙锁）锁住范围，不让别人插入。所以大多数场景不幻读，但有特例。
实测：对 `id>5` 执行 `FOR UPDATE` 后，别的事务往这个范围 `INSERT` 被阻塞，直到提交。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 252">
<text x="90" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事务 A</text>
<text x="254" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事务 B</text>
<line x1="170" y1="22" x2="170" y2="196" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<rect x="8" y="24" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1. 快照读 count = 2</text>
<rect x="180" y="58" width="152" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="256" y="75" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2. INSERT 一行并提交</text>
<rect x="8" y="92" width="156" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="109" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3. 快照读 count = 2</text>
<rect x="8" y="126" width="156" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86" y="143" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4. UPDATE 命中新行</text>
<rect x="8" y="160" width="156" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="86" y="177" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5. 快照读 count = 3</text>
<text x="8" y="224" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">加锁读（FOR UPDATE、UPDATE、DELETE）：</text>
<text x="8" y="242" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">next-key lock 锁住范围，别人插不进来</text>
</svg>
事务 A 先后看了三次：别人插入前后快照读都是 2，不幻读；但 A 的 `UPDATE` 碰到了 B 刚插入的那行，之后快照读变成 3，这就是 RR 里仍然可能出现的幻读。底部是加锁读的防护方式。
**举个例子。** 一个事务 A 统计满足某条件的行数：
1. **A 第一次快照读：** 满足条件的有 2 行，count 得 2。
2. **B 插入：** 事务 B 插入一行满足条件的数据并提交。
3. **A 再快照读：** 读的还是事务开始时的快照，count 仍然是 2，没有幻读。
4. **A 执行 UPDATE：** `UPDATE` 是当前读，能看到 B 刚提交的那行并改了它，这行的版本现在是 A 自己的。
5. **A 再快照读：** 自己改过的行当然看得到，count 变成 3，幻读出现。
6. **换成加锁读：** 如果 A 一开始就用 `SELECT ... FOR UPDATE` 读这个范围，next-key lock 会锁住范围，B 的 `INSERT` 被阻塞到 A 提交，A 全程看到的都是同一批行。
**容易错。**
- **以为 RR 完全解决了幻读：** 没有完全解决，快照读后自己 `UPDATE` 命中别人插入的行就是特例。
- **以为快照读也会加锁：** 不会，它只读历史版本，所以挡不住别人插入。
- **以为两种读可以随便混用：** 混用时看到的版本不同，行数也可能不同。
- **以为 RC 也有间隙锁：** RC 只有记录锁，当前读也会幻读。
- **用先查后插来避免重复：** 先查「有没有」再插入，两个事务都查到没有，各自插入。
- **以为对还不存在的行 FOR UPDATE 就能互斥：** 查不到行时拿到的只是间隙锁，间隙锁之间不冲突，两个事务都能拿到，随后各自插入时互相等对方的间隙锁，结果是死锁。要锁就锁已经存在的行（如库存行），最稳是唯一约束。
