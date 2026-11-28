---
id: bagu-exec-flow-engines-1-sql-flow-engines
node: b.mysql.exec-flow-engines
type: qa
step: 1
---
## Q
**一条 SQL 的执行流程与存储引擎**｜追问

面试官：「一条 SELECT 在 MySQL 内部经过哪些阶段？InnoDB 和 MyISAM 有什么区别？查询缓存为什么 8.0 删掉了？」

## A
**基本回答。** 连接器（认证、查权限、维护连接，空闲超过 `wait_timeout` 默认 8 小时就断开）→ 解析器（词法、语法分析）→ 优化器（选索引、定 join 顺序）→ 执行器（检查表权限，调存储引擎接口逐行取数据）。InnoDB 支持事务、行锁、崩溃恢复和聚簇索引；MyISAM 只有表锁、不支持事务。
前四步都在 Server 层，存取数据的是存储引擎，所以引擎可插拔；InnoDB 自 5.5.5 起是默认引擎，行格式默认 DYNAMIC。MyISAM 保存总行数，无条件 `count(*)` 很快；全文索引两者都支持（InnoDB 从 5.6 起）。查询缓存按完整 SQL 文本缓存，表一更新就整表失效，维护还要全局锁，收益小代价大，8.0 删除。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 272">
<rect x="10" y="8" width="100" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="29" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接器</text>
<text x="124" y="29" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">认证、查权限、管连接</text>
<line x1="60" y1="42" x2="60" y2="56" stroke="currentColor" stroke-width="1.2"/>
<polygon points="60,56 57.0,49.7 63.0,49.7" fill="currentColor"/>
<rect x="10" y="56" width="100" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">解析器</text>
<text x="124" y="77" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">词法、语法分析</text>
<line x1="60" y1="90" x2="60" y2="104" stroke="currentColor" stroke-width="1.2"/>
<polygon points="60,104 57.0,97.7 63.0,97.7" fill="currentColor"/>
<rect x="10" y="104" width="100" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="60" y="125" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">优化器</text>
<text x="124" y="125" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">选索引、定 join 顺序</text>
<line x1="60" y1="138" x2="60" y2="152" stroke="currentColor" stroke-width="1.2"/>
<polygon points="60,152 57.0,145.7 63.0,145.7" fill="currentColor"/>
<rect x="10" y="152" width="100" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="60" y="173" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">执行器</text>
<text x="124" y="173" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">查表权限，逐行调引擎</text>
<line x1="10" y1="204" x2="330" y2="204" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="330" y="198" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Server 层</text>
<text x="330" y="220" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">存储引擎层</text>
<line x1="60" y1="194" x2="60" y2="226" stroke="currentColor" stroke-width="1.2"/>
<polygon points="60,226 57.0,219.7 63.0,219.7" fill="currentColor"/>
<rect x="10" y="226" width="150" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="242.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">InnoDB</text>
<text x="85" y="257.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">事务·行锁·崩溃恢复</text>
<rect x="176" y="226" width="154" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="253" y="242.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MyISAM</text>
<text x="253" y="257.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">表锁·无事务</text>
</svg>
虚线以上是 Server 层的四个阶段，依次执行；虚线以下是存储引擎层，可以换；高亮的优化器是最容易选错索引的一步。
**举个例子。** 执行 `SELECT * FROM orders WHERE user_id = 7`：
1. **连接器：** 校验账号密码，确认你有权访问 `orders` 所在的库。
2. **解析器：** 切词并确认这是一条合法的 SELECT。
3. **优化器：** 发现 `user_id` 上有索引，估算后决定用它，而不是全表扫。
4. **执行器：** 检查表权限，调用 InnoDB 的接口，按索引一行行取回，直到取完。
5. **假如有查询缓存：** 只要 `orders` 被更新过一次，这张表的缓存就全部作废，写多的业务几乎命中不了，所以 8.0 干脆不做这层缓存。
**容易错。**
- **以为 MySQL 会缓存查询结果：** 8.0 已经没有查询缓存，要缓存就在应用层加 Redis。
- **以为优化器一定选最优索引：** 它按估算代价选，可能选错，要用 `EXPLAIN` 核对。
- **以为 MyISAM 更快所以更好：** 它只有表锁、不支持事务、崩溃要修复；只有无条件 `count(*)` 因为存了总行数而更快。
