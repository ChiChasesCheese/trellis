---
id: bagu-gap-deadlock-6-avoid
node: a.mysql.gap-deadlock
type: qa
step: 6
---
## Q
**避免死锁 · 加锁顺序、缩短事务、降低隔离级别**｜追问

面试官：「设计上怎么避免死锁？秒杀扣库存这种热点行更新怎么处理？」

## A
**基本回答。** 按重要性排：所有事务按相同顺序加锁（要锁多行就先按主键排序）；事务尽量短，不在事务里调远程服务；批量更新拆成每批几百行；条件走索引，缩小锁范围；业务能接受时用 RC，没有间隙锁；应用对 1213 做有限次重试，并保证操作幂等；「先查后插」改成直接插入加唯一索引。热点行（如秒杀库存只有一行）则要从架构上减少对同一行的竞争。
先查后插改成直接插入加唯一索引，用 duplicate key 拦截重复。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="80" y="8" width="180" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="25.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 万人同时下单</text>
<line x1="170" y1="34" x2="170.0" y2="43.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,50.0 166.8,43.0 173.2,43.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="30" y="50" width="280" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="67.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis Lua 原子预扣；失败直接返回</text>
<line x1="170" y1="76" x2="170.0" y2="85.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,92.0 166.8,85.0 173.2,85.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="80" y="92" width="180" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="109.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">成功者进库下单</text>
<line x1="170" y1="118" x2="170.0" y2="127.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,134.0 166.8,127.0 173.2,127.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="12" y="134" width="28" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="26.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="44" y="134" width="28" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="58.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="76" y="134" width="28" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="90.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="108" y="134" width="28" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="122.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="140" y="134" width="28" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="154.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="172" y="134" width="28" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="186.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="204" y="134" width="28" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="218.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<rect x="236" y="134" width="28" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="250.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<rect x="268" y="134" width="28" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="282.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<rect x="300" y="134" width="28" height="26" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--dim,#6b7280)"/>
<text x="314.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<text x="8" y="182" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">库存拆成 10 行，随机扣一桶</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">UPDATE stock SET n=n-1 WHERE id=? AND n&gt;0</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">放在事务最后一步，缩短持锁时间</text>
</svg>
一万个请求同时扣库存：先在 Redis 里用 Lua 脚本原子预扣，失败的直接返回，只有成功的才进库下单；库存本身再拆成 10 行（10 个桶），随机扣其中一桶，单行的竞争降到十分之一。
**举个例子。** 限量礼物抢购，库存只有一行，1 万人同时下单：
1. **原来的做法：** 1 万个请求都去 `UPDATE` 同一行，全部排在这一行的锁上，响应飙到秒级，还伴随超时。
2. **第一道闸：** Redis 里用原子 Lua 脚本预扣库存，扣不到的直接返回「已抢光」，成功的才进库。
3. **第二道分流：** 数据库里把一行库存拆成 10 个桶，请求随机扣其中一个，单行的竞争降到原来的十分之一。
4. **扣减写法：** `UPDATE stock SET n = n - 1 WHERE id = ? AND n > 0`，一条语句同时判断和扣减，库存不够时影响行数为 0，不会扣成负数。
5. **缩短持锁：** 这条更新放在事务的最后一步，拿到行锁后马上提交。
**容易错。**
- **以为加了重试就万事大吉：** 重试必须配合幂等，否则会重复扣款。
- **只调隔离级别不改顺序：** RC 只是减少间隙锁，行锁顺序相反照样死锁，根本办法是统一加锁顺序。
- **先查库存再改库存：** 查和改之间别人也在改，应该一条 `UPDATE ... WHERE n > 0` 完成。
- **以为热点行靠加机器解决：** 同一行排队，吞吐上限由单行决定；要靠预扣、分桶减少对同一行的竞争。
