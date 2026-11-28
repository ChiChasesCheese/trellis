---
id: bagu-db-consistency-6-strong
node: a.cache.db-consistency
type: qa
step: 6
---
## Q
**缓存一致性 · 要求强一致怎么办**｜追问

面试官：「价格和库存要求缓存与数据库强一致，旁路缓存能做到吗？」

## A
**基本回答。** 旁路缓存做不到强一致，只能缩短不一致的时间。要强一致的读，得换个思路：关键读绕过缓存，直接读主库（价格、库存、余额这类资金相关校验必须读库；缓存在 CAP 里选了可用性，接受最终一致，真强一致的数据放数据库事务里）。另两种办法：读写加同一把锁，互斥但吞吐明显下降；缓存存版本号，回填时用 Lua「比较并设置」，缓存已有价格 80（版本 5），慢线程拿着旧价 100（版本 4）想回填会被拒绝。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 244">
<rect x="8" y="8" width="120" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">商品列表页</text>
<text x="68" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">展示价格</text>
<rect x="212" y="8" width="120" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="22.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存</text>
<text x="272" y="37.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">可以略旧</text>
<line x1="128" y1="26" x2="206" y2="26" stroke-width="1.2" stroke="currentColor"/>
<polygon points="212.0,26.0 205.0,29.2 205.0,22.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="62" width="120" height="36" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="68" y="76.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">下单校验</text>
<text x="68" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">价格、库存</text>
<rect x="212" y="62" width="120" height="36" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="272" y="76.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">主库</text>
<text x="272" y="91.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">必须最新</text>
<line x1="128" y1="80" x2="206" y2="80" stroke-width="1.2" stroke="currentColor"/>
<polygon points="212.0,80.0 205.0,83.2 205.0,76.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">版本号：回填时比较并设置（Lua）</text>
<rect x="8" y="134" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="153" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">缓存 v5</text>
<rect x="120" y="134" width="100" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="153" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">旧读回填 v4</text>
<rect x="232" y="134" width="100" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="282" y="153" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">拒绝写入</text>
<line x1="108" y1="149" x2="114" y2="149" stroke-width="1.2" stroke="currentColor"/>
<polygon points="120.0,149.0 113.0,152.2 113.0,145.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="220" y1="149" x2="226" y2="149" stroke-width="1.2" stroke="currentColor"/>
<polygon points="232.0,149.0 225.0,152.2 225.0,145.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">读写同一把锁：吞吐明显下降，只给少量关键数据</text>
<text x="8" y="210" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">缓存当权威数据：要担丢数据风险，一般不推荐</text>
<text x="8" y="230" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">缓存是 AP，接受最终一致</text>
</svg>
上半是分流：展示用的读走缓存，下单校验走主库。中间是版本号的办法：缓存里已有较新的版本，较旧的回填会被拒绝。底部是另外两种办法和缓存的定位。
**容易错。**
- **以为加锁就能换来强一致还不影响性能：** 锁让读写互斥，吞吐明显下降，只能给少量关键数据。
- **以为版本号万能：** key 被删后没有版本可比，旧线程仍能回填旧值，删除时要留一个短期的版本标记。
- **让缓存决定扣库存：** 资金、库存的校验必须读库。
- **想着缓存和数据库永远一致：** 只能做到最终一致，并缩短窗口。
- **缓存当权威数据不推荐：** 把缓存当权威数据（只写 Redis 并持久化，异步落库），要承担丢数据的风险，一般不推荐。

**业务场景。** 下单前校验价格直接读主库，商品列表页读缓存，用户即使在列表看到旧价，下单时仍以主库价为准。
