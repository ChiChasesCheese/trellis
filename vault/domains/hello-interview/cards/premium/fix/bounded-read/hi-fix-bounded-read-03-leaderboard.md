---
id: hi-fix-bounded-read-03-leaderboard
node: fix.bounded-read
type: qa
step: 3
---
## Q
**在线游戏排行榜 · 有界读**｜补强

面试官：「在线游戏，一亿玩家。要显示全球前 10、玩家自己的名次，以及自己前后各 5 名；打完一局 1 到 2 秒内更新。怎么读、怎么写？」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **先说结构：** 「一个有序集合 `lb:{game}:all`，成员是 player_id，分数就是排序键。」
- **读前 10 名：** 「`ZRANGE lb 0 9 REV WITHSCORES`（等价于 `ZREVRANGE lb 0 9 WITHSCORES`）。所有人看到同一份，API 实例本地缓存 1 秒。」
- **读我的名次：** 「`ZREVRANK lb me` 返回从 0 起算的名次 r，显示 r+1。」
- **读前后各 5 名：** 「`ZRANGE lb max(r-5,0) r+5 REV WITHSCORES`，超出末尾的部分 Redis 会自动忽略。读的条数固定，和一亿玩家无关。」
- **写：** 「打完一局，先写数据库保存最高分，再 `ZADD lb GT <分数> <player>`。`GT` 只在新分更高时才更新，是绝对值写，重放、重试都无害。我不用 `ZINCRBY`：重试会把分数加两次。」
- **为什么不裁剪：** 「要查任何玩家的名次，所以整个集合都留着；读是有界的，结构不用裁。一亿成员按每个约 100 字节，大约 10 GB，一台放得下。」
- **同分怎么排：** 「Redis 同分时按成员字典序，没有业务含义。要「先达到的靠前」，就把时间编进分数：整数分数必须小于 2 的 53 次方，因为分数是双精度浮点数。比如竞赛：`解题数 × 10^7 − 罚时秒数`。」
- **丢了怎么重建：** 「从最高分表扫一遍灌进去；它是派生数据，数据库才是真相。」
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 258">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">一个有序集合 lb:{game}:all</text>
<rect x="8" y="26" width="324" height="62" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="46" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">前 10 名</text>
<text x="18" y="61" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZRANGE lb 0 9 REV WITHSCORES</text>
<text x="18" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">所有人看到同一份，可本地缓存 1 秒</text>
<text x="170" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">⋮  中间的人不读  ⋮</text>
<rect x="8" y="126" width="324" height="78" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="154" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">我的名次与前后各 5 名</text>
<text x="18" y="169" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">r = ZREVRANK lb me（从 0 起）</text>
<text x="18" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZRANGE lb max(r-5,0) r+5 REV WITHSCORES</text>
<text x="8" y="228" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">显示名次 = r + 1；读的条数固定，</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">与玩家总数无关（对数时间 + 约 11 条）</text>
</svg>
白板上：前 10 和我的前后 5 名，都是对同一个有序集合的固定大小读取。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 286">
<rect x="8" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="44" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">游戏服务器</text>
<rect x="92" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="128" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">分数服务</text>
<rect x="176" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="212" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据库</text>
<rect x="262" y="8" width="72" height="38" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="298" y="31" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Redis</text>
<text x="48" y="72" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">提交 (玩家, 分数)</text>
<polyline points="44,84 128,84" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="128,84 121.0,87.2 121.0,80.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">只在更高时更新最高分</text>
<polyline points="128,118 212,118" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="212,118 205.0,121.2 205.0,114.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="140" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZADD lb GT 分数 玩家</text>
<polyline points="128,152 298,152" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,152 291.0,155.2 291.0,148.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="180" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">重试 / 重放同一条</text>
<text x="48" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">提交 (玩家, 分数)</text>
<polyline points="44,214 128,214" fill="none" stroke-width="1.3" stroke="currentColor"/>
<polygon points="128,214 121.0,217.2 121.0,210.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="132" y="236" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">ZADD lb GT …：分数不变</text>
<polyline points="128,248 298,248" fill="none" stroke-width="1.3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="298,248 291.0,251.2 291.0,244.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="274" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">绝对值，不用 ZINCRBY</text>
<line x1="44" y1="48" x2="44" y2="263" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="44" y1="278" x2="44" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="48" x2="128" y2="61" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="76" x2="128" y2="169" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="184" x2="128" y2="191" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="206" x2="128" y2="263" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="128" y1="278" x2="128" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="48" x2="212" y2="95" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="110" x2="212" y2="129" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="144" x2="212" y2="169" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="184" x2="212" y2="225" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="212" y1="240" x2="212" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="298" y1="48" x2="298" y2="282" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="8" y1="176" x2="108.2" y2="176" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
<line x1="231.8" y1="176" x2="332" y2="176" stroke-width="1" stroke-dasharray="5 4" style="stroke:var(--dim,#6b7280)"/>
</svg>
白板上：写用 GT 的绝对值，重放不会改变分数。

**为什么这样说。** 面试官要看的是：读的命令是否真的有界，写是否能承受重试。弱的回答是 `ORDER BY score DESC LIMIT 10` 加 `COUNT(*) WHERE score > x` 查名次：名次那个查询是对一亿行的计数，不可能撑住每秒上万次。强的回答给出 `ZREVRANK` 加区间读，并说明整个集合保留是因为需要任意玩家的名次。
**面试官可能接着问。**
- 一台放不下怎么办？ → 按分数区间拆分，不按玩家哈希：全局名次 = 分数更高的各片的成员数之和 + 片内名次；各片的 `ZCARD` 缓存几秒。
- 好友榜怎么做？ → 读时计算：取好友列表，对全球集合 `ZMSCORE` 批量查分，在应用里排序；不要在写时扇出到每个好友。
- 日榜周榜呢？ → 每个周期一个键，用 `EXPIRE` 过期；分数写两个键。
- 榜单要多新？ → 打完一局后同步写 Redis，1 到 2 秒内可见；前 10 名的本地缓存会多等 1 秒。
**常见失分。**
- **用 `ZINCRBY` 累加：** 重试把分数加两次。
- **用数据库查名次：** 对大表的名次查询不可能每秒几万次。
- **按玩家哈希分片：** 每片只有局部顺序，名次要合并所有分片。
- **把分数编码超出 2 的 53 次方：** 浮点精度丢失，不同的分数变成相同。
