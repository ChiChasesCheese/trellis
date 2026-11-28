---
id: bagu-isolation-levels-2-anomalies
node: a.mysql.isolation-levels
type: qa
step: 2
---
## Q
**三种并发问题 · 脏读、不可重复读、幻读各举一个例子**｜必会

面试官：「脏读、不可重复读、幻读，用转账或对账的例子各讲一个，别讲定义。」

## A
**基本回答。** 脏读：事务 A 把余额 100 扣到 50 还没提交，事务 B 读到 50 去做判断，之后 A 回滚，B 依据的是一个从没真正存在过的值。不可重复读：对账任务在同一个事务里先读余额是 100，期间用户提现 50 并提交，任务再读就变成 50。幻读：先统计「今日打赏笔数」得 1000，期间有新打赏提交，再统计变成 1001。
8.0 两会话演示：RC 下 A 读 `id=1` 为 100，B 改成 200 并提交，A 再读得 200；RR 下仍是 100。RC 下第二次 `COUNT` 从 3 变成 4，RR 下仍是 3。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 224">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">脏读：读到没提交的</text>
<rect x="8" y="20" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="34.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B 改 100→50</text>
<text x="58.0" y="49.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">还没提交</text>
<line x1="108" y1="38" x2="113.0" y2="38.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,38.0 113.0,41.2 113.0,34.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="20" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="42.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 读到 50</text>
<line x1="220" y1="38" x2="225.0" y2="38.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,38.0 225.0,41.2 225.0,34.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="20" width="100" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282.0" y="34.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B 回滚</text>
<text x="282.0" y="49.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50 从没存在</text>
<text x="8" y="78" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">不可重复读：已有行的值变了</text>
<rect x="8" y="84" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 读余额</text>
<text x="58.0" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">100</text>
<line x1="108" y1="102" x2="113.0" y2="102.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,102.0 113.0,105.2 113.0,98.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="84" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B 提现 50</text>
<text x="170.0" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">并提交</text>
<line x1="220" y1="102" x2="225.0" y2="102.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,102.0 225.0,105.2 225.0,98.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="84" width="100" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282.0" y="98.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 再读</text>
<text x="282.0" y="113.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">50，值变了</text>
<text x="8" y="142" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">幻读：满足条件的行变了</text>
<rect x="8" y="148" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58.0" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 统计笔数</text>
<text x="58.0" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1000</text>
<line x1="108" y1="166" x2="113.0" y2="166.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,166.0 113.0,169.2 113.0,162.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="120" y="148" width="100" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B 新增一笔</text>
<text x="170.0" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">并提交</text>
<line x1="220" y1="166" x2="225.0" y2="166.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,166.0 225.0,169.2 225.0,162.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="232" y="148" width="100" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282.0" y="162.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A 再统计</text>
<text x="282.0" y="177.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1001，多了行</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">变的对象不同：未提交值 / 已有行 / 行集合</text>
</svg>
三行各是一个时间顺序：脏读是 B 还没提交，A 就读到了；不可重复读是 A 前后两次读同一行，中间 B 提交了修改；幻读是 A 前后两次统计，中间 B 新增了一行。每一行右边高亮的一格就是出问题的那一步。
**举个例子。** 以对账为例，逐步看三种问题：
1. **脏读：** B 把余额从 100 扣到 50，没提交；A 读到 50，用它做了判断；B 回滚，余额其实还是 100，A 的判断建立在假数据上。
2. **不可重复读：** 对账任务（事务 A）先读余额 100；用户提现 50 并提交；任务再读，余额变成 50，同一事务里两次读不一致。
3. **幻读：** 任务先 `COUNT` 今日打赏笔数得 1000；这时新打赏提交；再 `COUNT` 得 1001，多出了一行。
4. **换成 RR：** 同样的顺序，第二次读余额仍是 100，第二次 `COUNT` 仍是 1000，因为事务一直在看第一次读时那份快照。
**容易错。**
- **把不可重复读和幻读混为一谈：** 前者是同一行的值变了，后者是满足条件的行数变了；防法也不同，后者要锁范围。
- **以为脏读在 RC 下也会出现：** 脏读只在读未提交出现，RC 及以上读到的都是已提交数据。
- **以为幻读只看「新增」：** 行被删掉导致集合变小也算，本质是「行集合变了」。
- **以为 RR 下一定读到旧值：** 这里说的是快照读；加锁的当前读读的是最新数据（后面的卡片会讲）。
**业务场景。** 日终对账要事务内前后一致，先查总额再按明细汇总。用 RC 时两次读之间有新入账，总额和明细差一笔，对账误报不平；应使用 RR，或把截止时间写进查询条件。
