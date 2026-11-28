---
id: bagu-gap-deadlock-3-insert-block
node: a.mysql.gap-deadlock
type: qa
step: 5
---
## Q
**间隙锁为什么会让并发插入阻塞**｜追问

面试官：「间隙锁怎么阻塞别人插入？插入意向锁是什么？为什么间隙锁之间不冲突却会引起死锁？」

## A
**基本回答。** 事务往某个间隙里插入之前，要先申请插入意向锁（insert intention lock），这是一种特殊的间隙锁，表示「我要往这个间隙的某个位置插入」。它会和别人持有的间隙锁、next-key 锁冲突，所以被挡住等待；多个插入意向锁之间，只要插入的位置不同就不冲突；间隙锁和间隙锁之间也不冲突。
复现死锁（8.0.46，表里有 id=1 和 10）：A `WHERE id=5 FOR UPDATE`、B `WHERE id=6 FOR UPDATE`，都在 `(1, 10)` 拿到间隙锁；A 插入 4、B 插入 7，插入意向锁各被对方挡住，InnoDB 检测到环后回滚一个。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事务 A</text>
<text x="182" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">事务 B</text>
<rect x="8" y="22" width="150" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83.0" y="36.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SELECT id=5</text>
<text x="83.0" y="51.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">FOR UPDATE → 间隙锁</text>
<rect x="182" y="66" width="150" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="257.0" y="80.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">SELECT id=6</text>
<text x="257.0" y="95.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">FOR UPDATE → 间隙锁</text>
<rect x="8" y="110" width="150" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83.0" y="124.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INSERT 4</text>
<text x="83.0" y="139.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">意向锁被 B 挡住</text>
<rect x="182" y="154" width="150" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="257.0" y="168.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">INSERT 7</text>
<text x="257.0" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">意向锁被 A 挡住</text>
<line x1="83" y1="58" x2="83.0" y2="103.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,110.0 79.8,103.0 86.2,103.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="257" y1="102" x2="257.0" y2="147.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="257.0,154.0 253.8,147.0 260.2,147.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">原有 id=1、10，两把间隙锁都在 (1,10)</text>
<rect x="8" y="224" width="324" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="243.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 等 B，B 等 A → 1213，回滚一个</text>
</svg>
两个事务先后对 (1,10) 这段间隙加了间隙锁（互不冲突）；接着 A 要插入 4、B 要插入 7，各自的插入意向锁都被对方的间隙锁挡住，A 等 B、B 等 A，成环，InnoDB 检测到后报 1213 并回滚一个。
**举个例子。** 「先查是否存在，不存在才插入」的写法，表里已有 id=1 和 10：
1. **A 先查：** `SELECT ... WHERE id=5 FOR UPDATE`，没有这一行，拿到 `(1,10)` 的间隙锁。
2. **B 也查：** `WHERE id=6 FOR UPDATE`，也没有，也拿到 `(1,10)` 的间隙锁，不冲突，两边都拿到。
3. **A 插入 4：** 申请插入意向锁，被 B 持有的间隙锁挡住，等待。
4. **B 插入 7：** 申请插入意向锁，被 A 持有的间隙锁挡住，等待。
5. **成环：** A 等 B，B 等 A；InnoDB 检测到环，回滚其中一个，报 1213，另一个继续。
6. **正确写法：** 直接 `INSERT`，靠唯一索引拦截重复，捕获 duplicate key；或用 `INSERT ... ON DUPLICATE KEY UPDATE`。
**容易错。**
- **以为间隙锁会互相冲突：** 它们不互斥，这正是死锁的前提。
- **以为间隙锁会阻止读和更新：** 它只阻塞往间隙里的插入。
- **以为先查后插是安全的：** 两个并发请求都查不到，都拿到同一间隙的间隙锁，再各自插入就会死锁。
- **把死锁归咎于数据库：** 根因是业务用了「先 `FOR UPDATE` 查再插」的写法，应改成直接插入加唯一索引。
