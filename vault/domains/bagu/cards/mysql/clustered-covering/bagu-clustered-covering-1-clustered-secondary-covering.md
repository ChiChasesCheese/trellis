---
id: bagu-clustered-covering-1-clustered-secondary-covering
node: b.mysql.clustered-covering
type: qa
step: 1
---
## Q
**聚簇索引与二级索引 · 回表、覆盖、下推与自增主键**｜必会

面试官：「聚簇索引和二级索引有什么区别？什么是回表、覆盖索引、索引下推？主键为什么推荐自增，自增值为什么会不连续？」

## A
**基本回答。** 聚簇索引（主键索引）的叶子存整行数据；二级索引的叶子存「索引列 + 主键值」，查整行要拿主键再去聚簇索引查一次，叫回表。查询的列都在二级索引里就是覆盖索引，不用回表。索引下推（ICP，5.6+）让引擎先用索引里的列过滤，再回表。
没有主键时：InnoDB 选第一个非空唯一索引当聚簇索引，再没有就用隐藏的 6 字节行 ID。EXPLAIN 的 Extra：`Using index` 是覆盖，`Using index condition` 是下推。主键要短：每个二级索引叶子都存一份主键，UUID 占 16 到 36 字节。自增值会不连续：唯一键冲突、回滚、批量预分配都会用掉号（实测 8.0.46，id 从 1 跳到 4）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 260">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SELECT * FROM orders WHERE phone = ?</text>
<rect x="8" y="24" width="146" height="64" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="81" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">二级索引（phone）</text>
<text x="81" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶子存 phone + 主键值</text>
<text x="81" y="75" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">phone → id = 7</text>
<line x1="154" y1="56" x2="184" y2="56" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="184,56 177,59.2 177,52.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="184" y="24" width="148" height="64" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="258" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">聚簇索引（主键 id）</text>
<text x="258" y="60" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶子存整行数据</text>
<text x="258" y="75" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">id = 7 → 整行</text>
<text x="8" y="108" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1. 二级索引先找到 id = 7</text>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">2. 拿 id 去聚簇索引再查一次 = 回表</text>
<text x="8" y="154" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">SELECT id, phone ... WHERE phone = ?</text>
<text x="8" y="172" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">要的列都在二级索引叶子里 → 不回表</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Extra: Using index = 覆盖索引</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Extra: Using index condition = 索引下推</text>
<text x="8" y="232" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">自增主键追加到最右叶子；UUID 插中间</text>
<text x="8" y="250" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">UUID 引起页分裂，页利用率降到约一半</text>
</svg>
先在二级索引里按 phone 找到主键 id，再拿 id 去聚簇索引取整行，这一步就是回表；如果要的列二级索引里本来就有，第二步可以省掉。图的最后两行是主键选择对插入的影响。
**举个例子。** 订单表 `orders`，主键 `id`，二级索引 `idx_phone(phone)`：
1. **按手机号查整行：** `select * ... where phone='138...'`，先在 `idx_phone` 找到这个手机号对应的主键 `id = 7`（叶子存的是 phone 和主键值）。
2. **回表：** 拿 `id = 7` 去聚簇索引取整行。如果这个条件命中 1000 行，就要回表 1000 次，每次都是一次随机读。
3. **改成只查 id 和 phone：** `select id, phone ... where phone=?`，这两列都在 `idx_phone` 的叶子里，不用回表，Extra 显示 `Using index`。
4. **把常查字段放进联合索引：** 常查金额的话建 `(phone, amount)`，查 phone 返回 amount 也走覆盖索引。
5. **自增跳号：** 先成功插入一条，id 为 1；再来一条因唯一键冲突失败，用掉 2；再来一条事务回滚，用掉 3；下一条成功拿到 4。
**容易错。**
- **以为二级索引叶子存整行：** 它只存索引列和主键值，所以才需要回表。
- **以为回表一定有问题：** 命中几行时代价很小，命中行数多时才是大问题。
- **以为覆盖索引越多越好：** 索引变大、写入变慢，只给高频查询建。
- **以为自增 id 是连续的：** 唯一键冲突、回滚、批量插入预分配都会跳号。
- **混淆两种 Using index：** 前者是覆盖，后者是索引下推。
