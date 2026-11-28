---
id: bagu-lock-types-1-lock-classification
node: b.mysql.lock-types
type: qa
step: 1
---
## Q
**MySQL 锁分类 · 意向锁、元数据锁与乐观悲观锁**｜追问

面试官：「MySQL 有哪几类锁？意向锁是干什么的？为什么给大表加字段会让整张表的查询都卡住？」

## A
**基本回答。** 按粒度分：全局锁（备份用）、表锁、元数据锁（MDL）、意向锁、行锁（记录锁、间隙锁、next-key 锁）。按策略分：悲观锁先锁后改（`SELECT ... FOR UPDATE`），乐观锁不加锁，用 `UPDATE ... WHERE version = ?` 看影响行数。
行锁只有 InnoDB 有，MyISAM 只有表锁。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">MDL 排队：长事务 → ALTER → 后续查询</text>
<rect x="8" y="24" width="96" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长事务</text>
<text x="56" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">持有 MDL 读锁</text>
<line x1="120" y1="44" x2="104" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="104,44 111,40.8 111,47.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="24" width="96" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="168" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ALTER TABLE</text>
<text x="168" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">要独占 MDL</text>
<line x1="232" y1="44" x2="216" y2="44" stroke-width="1.2" stroke="currentColor"/>
<polygon points="216,44 223,40.8 223,47.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="24" width="100" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">后面的 SELECT</text>
<text x="282" y="55.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">排在它后面</text>
<text x="8" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">实测：Waiting for table metadata lock</text>
<text x="8" y="112" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">按粒度分的几类锁</text>
<rect x="8" y="120" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全局锁</text>
<rect x="73" y="120" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="103" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">表锁</text>
<rect x="138" y="120" width="60" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="168" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MDL</text>
<rect x="203" y="120" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="233" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">意向锁</text>
<rect x="268" y="120" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="298" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">行锁</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">行锁加在索引上，没走索引会锁住大得多的范围</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">悲观锁：先锁后改 SELECT ... FOR UPDATE</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">乐观锁：UPDATE ... WHERE version = ?</text>
</svg>
上半部分是加字段堵住整张表的过程：长事务持有 MDL 读锁，`ALTER` 要独占，只能排队，后面的普通查询又排在 `ALTER` 后面；下半部分是 MySQL 里按粒度划分的几类锁，以及悲观锁和乐观锁的写法。
**举个例子。** 高峰期给大表加字段：
1. **长事务在先：** 事务 A 开始后查询了 `orders`，一直没提交，持有 `orders` 的 MDL 读锁。
2. **ALTER 排队：** 运维执行 `ALTER TABLE orders ...`，需要独占 MDL，被 A 挡住，状态是 `Waiting for table metadata lock`。
3. **后续查询排队：** 之后所有 `SELECT` 也要拿 MDL，排在 `ALTER` 后面，一起等。
4. **整表不可用：** 连接越堆越多，很快被占满。
5. **预防：** DDL 避开高峰，执行前先查有没有长事务，并把 `lock_wait_timeout` 设短，让 DDL 失败而不是堵住线上。
6. **乐观出价的写法：** 拍卖出价用 `UPDATE ... WHERE price < ?`，影响行数为 0 就说明别人已经出了更高的价。
**容易错。**
- **以为 DDL 只影响它自己：** 它会堵住排在它后面的所有普通查询。
- **以为意向锁会阻止别人加行锁：** 意向锁之间不冲突，它只是给表锁请求看的一个声明。
- **以为行锁锁的是行：** 实际加在索引上，没走索引会锁住大得多的范围。
- **以为乐观锁没有代价：** 冲突多时重试成本高，该用悲观锁。
- **以为 lock_wait_timeout 有合理默认：** 默认是一年，不设短等于不超时。
