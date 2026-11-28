---
id: hi-fix-asked-race-03-three-tools
node: fix.asked-race
type: qa
step: 3
---
## Q
**先答被问的竞态 · 键、条件写、锁**｜补强

面试官：「幂等键、条件更新、加锁，你为什么在这个钱包里选条件更新来防两笔提现？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说各自回答的问题：** 「幂等键回答这个动作做过没有；条件写回答共享状态现在够不够；锁回答多行的联合条件谁先进。」
- **两笔不同的提现是第二个问题：** 「它们是两个动作，所以幂等键没用；条件只涉及钱包这一行的一个数，条件写一条语句就够，不用持锁。」
- **条件写的好处：** 「检查和占用是同一条语句，没有读和写之间的缝；行锁只在这条语句里持有，语句一结束就放。」
- **什么时候才用锁：** 「条件跨多行，比如转账要同时扣 A 加 B，或者要抢连号的座位。这时先按固定顺序给涉及的行加锁，再检查再写，避免死锁。」
- **锁的纪律：** 「持锁期间不调外部；Redis 里的锁会过期，数据库的约束才是最后一道。」
- **提现的最终组合：** 「attempt_id 唯一键挡重复，条件 UPDATE 挡竞态，两个在同一个事务里；用不到锁。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 276">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">三个工具，各回答一个问题</text>
<rect x="8" y="26" width="324" height="74" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">幂等键（Idempotency Key）</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">问：这个动作是不是已经做过？</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">唯一约束 + 返回第一次的结果</text>
<text x="18" y="89.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">管不了：两个不同的动作争同一份状态</text>
<rect x="8" y="108" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">条件写（Conditional Write）</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">问：这份共享状态现在够不够？</text>
<text x="18" y="156.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">UPDATE … WHERE 条件，看行数</text>
<text x="18" y="171.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">管不了：同一个动作重发，会各扣一次</text>
<rect x="8" y="190" width="324" height="74" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">锁（Lock）</text>
<text x="18" y="223.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">问：多行的联合条件，谁先进？</text>
<text x="18" y="238.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先锁相关的行，再检查，再写</text>
<text x="18" y="253.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">代价：占连接、会阻塞、会死锁</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 201">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">钱包提现用哪个</text>
<rect x="8" y="26" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">重复点击</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">attempt_id 唯一键</text>
<rect x="8" y="78" width="324" height="44" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="96.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">两笔不同的提现</text>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">条件 UPDATE ready_to_use &gt;= 金额</text>
<rect x="8" y="130" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="148.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">钱包 A 转给钱包 B（多行）</text>
<text x="18" y="163.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">按 wallet_id 升序加行锁，或放进同一事务</text>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">锁不跨支付平台调用</text>
</svg>
白板上：三个工具三行，下面是钱包里三种情形各用哪一个。
**为什么这样说。** （约 1 分钟。）面试官要听的是选择的依据。强的回答先说每个工具回答的问题，再说为什么这个案例落在条件写上；弱的回答是「加个分布式锁」，并且没有说锁什么、锁多久。
**面试官可能接着问。**
- 条件写不就是乐观并发吗？ → 乐观并发读出版本号，写时检查，输了要重读重试；这里条件就是业务条件，输了直接拒绝，不用重试。
- 为什么不用分布式锁？ → 它是另一个要保证可用的系统，锁会过期，过期后两个请求仍能同时进；数据库的一条语句不需要它。
- 冲突很多时呢？ → 同一个钱包的冲突本来很少；热点账户（比如平台费用账户）才需要分桶。
**常见失分。**
- **用幂等键答竞态：** 两个不同的动作，键不同，都通过。
- **用锁答每个问题：** 占连接、拖慢吞吐，却没有解决根本的原因。
- **持锁去调外部：** 外部一慢，行锁一直占着，后面的请求全部排队。
