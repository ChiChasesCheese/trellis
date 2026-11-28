---
id: hi-fix-component-cost-09-job-cost-trigger
node: fix.component-cost
type: qa
step: 9
---
## Q
**Airbnb Wallet · 加组件：作用、代价、触发**｜补强

面试官：「你的钱包设计里想加缓存、队列、分片。每一个说一下，为什么现在加。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **固定句式：** 「加 X。作用是……；代价是……；我在……时才加。」三句填不全，这个组件先不画。
- **Redis 缓存余额：** 「作用是挡余额的读；代价是多一份副本，会和库不一致，要用写后删或 SET 持久值来收敛；我在读超过 10,000 次/秒，或主库读延迟超目标时才加。现在读峰值 231 × 3 ≈ 700 次/秒，按主键读，不加。」
- **刷新队列：** 「作用是让用户的读不等支付平台；代价是任务会重复、会丢，用 transaction_id 去重，每日扫描兜底；触发条件已经满足，因为用户的读会触发外部调用，所以现在就加。」
- **分片：** 「作用是让写或存储超过单库；代价是跨分片事务没有了，钱包到钱包的转账会变难；我在写到数千次/秒，或热数据到几 TB 时才考虑。现在写峰值约 50 笔/秒，7 年 1.8 TB，不加。」
- **结论一句：** 「三个里只有队列现在要加；缓存和分片我只留下触发条件。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 231">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">钱包里想加的三样，各填三句</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">Redis 缓存余额</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">作用：挡余额读；代价：多一份副本，会不一致</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：读 &gt; 10,000 次/秒。现在 700：不加</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">刷新队列（调支付平台）</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">作用：用户读不等外部；代价：重复、丢任务</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：用户读会调外部，现在就加</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">分片</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">作用：写或存储超过单库；代价：跨分片事务</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发：写数千次/秒。现在 50，1.8 TB：不加</text>
</svg>

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 119">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发条件对着数字</text>
<rect x="8" y="26" width="102.67" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="59.33" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">读</text>
<text x="59.33" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">现在 700/秒</text>
<text x="59.33" y="74.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发 10,000/秒</text>
<rect x="118.67" y="26" width="102.67" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="170" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">写</text>
<text x="170" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">现在 50/秒</text>
<text x="170" y="74.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发 数千/秒</text>
<rect x="229.33" y="26" width="102.67" height="59" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="280.67" y="44.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" font-weight="bold">存储</text>
<text x="280.67" y="59.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">现在 1.8 TB</text>
<text x="280.67" y="74.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">触发 数 TB</text>
<text x="8" y="113" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">三句填不全，先不画；留一句「到了什么数再加」</text>
</svg>
白板上：每个组件三行，旁边把触发条件和现在的数字并排写。
**为什么这样说。** （约 1 分钟。）面试官要看你的设计是不是由数字推出来的。强的回答能把「不加」说成一个决定，并带着触发条件；弱的回答要么什么都加，要么什么都不敢说。
**面试官可能接着问。**
- 面试官说「再大 100 倍呢」？ → 读 70,000 次/秒，加缓存；写 5,000 笔/秒，开始看热点行和分片；这正是触发条件被满足的时候。
- 为什么队列算「现在就加」？ → 因为不加的话，外部调用要放进用户的读里，这是被明确指出的问题，不是规模问题。
- 缓存的触发为什么是 10,000 次/秒？ → 这是我的估计：带索引的主键读在亚毫秒到几毫秒，单库扛一万次/秒的简单读并不吃力；以实测为准，我会说出来是假设。
**常见失分。**
- **只有作用：** 没说代价，面试官问「那它出问题怎么办」就答不上。
- **触发条件是「流量大了」：** 没有数字，不是触发条件。
- **每个都加：** 700 次/秒的读，加缓存是自找麻烦。
