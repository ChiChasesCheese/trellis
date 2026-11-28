---
id: hi-fix-component-cost-08-five-questions
node: fix.component-cost
type: qa
step: 8
---
## Q
**五道题 · 加组件先说职责和新问题**｜补强

面试官：「你的设计里加了不少组件。把每一个的新问题和处理，再对我说一遍。」

你会怎么回答？白板上画到哪一步？

## A
**你说。**
- **GoFundMe：** 「Redis 为了读总额，新问题是副本不一致；我 SET 持久化值。队列为了不堵支付路径，新问题是重放；我用 applied 唯一键。」
- **Ticketmaster：** 「Redis 占座为了不锁数据库行，新问题是锁会过期；最终由数据库条件更新判定。」
- **Uber：** 「Redis 地理索引为了快速找附近的司机，新问题是数据短命；用 last_seen 清理，重启自己长回。」
- **Ad Click：** 「队列和流处理为了吸收峰值，新问题是重发和迟到；每个分区一个 applied offset，加水位线。」
- **News Feed：** 「预计算 feed 为了读得快，新问题是大 V 的写放大；大 V 不扩散，读时合并。」
- **共同点：** 处理这一格，永远落在一个具体的记录或规则上：唯一键、条件更新、last_seen、offset、阈值。说不出记录，就还没处理。
**白板。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 363">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">同一句话，五道题</text>
<rect x="8" y="26" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="44.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">GoFundMe · Redis + 队列</text>
<text x="18" y="59.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新问题：副本不一致、事件重放</text>
<text x="18" y="74.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">SET 持久化值；applied 唯一键</text>
<rect x="8" y="93" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="111.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Ticketmaster · Redis 占座</text>
<text x="18" y="126.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新问题：锁过期时人还在付款</text>
<text x="18" y="141.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">数据库条件更新做最终判定</text>
<rect x="8" y="160" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="178.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Uber · Redis 位置索引</text>
<text x="18" y="193.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新问题：数据短命，司机掉线</text>
<text x="18" y="208.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">last_seen 清理；重启自己长回</text>
<rect x="8" y="227" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="245.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">Ad Click · 队列 + 流处理</text>
<text x="18" y="260.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新问题：重发、乱序、迟到</text>
<text x="18" y="275.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">offset 随结果提交；水位线</text>
<rect x="8" y="294" width="324" height="59" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="18" y="312.5" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">News Feed · 预计算 feed</text>
<text x="18" y="327.5" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">新问题：大 V 写放大</text>
<text x="18" y="342.5" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">大 V 不扩散，读时合并</text>
</svg>
白板上：五行，每行一个组件、一个新问题、一个处理。
**为什么这样说。** （约 1 分钟，用在设计收尾时。）面试官通常在最后让你复盘权衡。强的回答把每个组件的新问题和处理说成同一个句式，让他不用再追问；弱的回答是把组件名再念一遍。
**面试官可能接着问。**
- 这些组件哪个最容易出事？ → 凡是「同一个事实写在两处」的：数据库和 Redis、数据库和队列。它们之间的窗口，就是我要用唯一键或条件更新收口的地方。
- 时间不够，只能讲一个，讲哪个？ → 挑最容易出错、而且面试官最可能追问的那个，讲完整的四格；其余一句话带过。
- 有没有加了但其实不需要的组件？ → 有。规模小的时候，在同一个事务里更新就够了，不需要队列。我先说不加的版本，再说为什么要加。
**常见失分。**
- **只在被问时才说新问题：** 主动说，是 senior 的表现。
- **处理是模糊的词：** 「保证一致」「做好重试」没有记录。
- **所有组件一视同仁地讲：** 要把时间花在最容易出错的那个上。
