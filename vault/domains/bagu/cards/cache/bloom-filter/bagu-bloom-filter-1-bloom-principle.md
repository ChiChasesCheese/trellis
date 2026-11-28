---
id: bagu-bloom-filter-1-bloom-principle
node: b.cache.bloom-filter
type: qa
step: 1
---
## Q
**布隆过滤器 · 原理、误判与选参**｜追问

面试官：「布隆过滤器的原理是什么，为什么会误判但不会漏判？位数组和哈希函数个数怎么选，能删除元素吗？」

## A
**基本回答。** 布隆过滤器（Bloom filter）由一个 m 位的位数组和 k 个哈希函数组成：添加一个元素，就用 k 个哈希函数各算出一个位置，把这 k 个位置都置 1；查询时算出同样的 k 个位置，全是 1 才回答「可能存在」，只要有一位是 0 就一定不存在。误判是因为别的元素恰好把这些位置凑成了 1，所以它只会误判（说有但其实没有），不会漏判（说没有但其实有）。它不能删除元素，因为一个位可能被多个元素共用。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">12 位，3 个哈希：a→位 2、5、9</text>
<text x="8" y="30" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">b→位 5、7、10</text>
<rect x="14" y="70" width="26" height="28" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="27.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="27" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="40" y="70" width="26" height="28" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="53.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="53" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="66" y="70" width="26" height="28" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="79.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="79" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="92" y="70" width="26" height="28" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="105.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="105" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="118" y="70" width="26" height="28" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="131.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="131" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="144" y="70" width="26" height="28" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="157.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="157" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="170" y="70" width="26" height="28" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="183.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="183" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="196" y="70" width="26" height="28" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="209.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="209" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<rect x="222" y="70" width="26" height="28" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="235.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="235" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">8</text>
<rect x="248" y="70" width="26" height="28" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="261.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="261" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">9</text>
<rect x="274" y="70" width="26" height="28" rx="0" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="287.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="287" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">10</text>
<rect x="300" y="70" width="26" height="28" rx="0" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="313.0" y="88.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="313" y="114" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">11</text>
<line x1="79" y1="46" x2="79" y2="68" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="79.0,68.0 75.8,61.0 82.2,61.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="209" y1="46" x2="209" y2="68" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="209.0,68.0 205.8,61.0 212.2,61.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="261" y1="46" x2="261" y2="68" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="261.0,68.0 257.8,61.0 264.2,61.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="14" y="62" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">查 c</text>
<line x1="105" y1="150" x2="105" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="105.0,122.0 108.2,129.0 101.8,129.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="157" y1="150" x2="157" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="157.0,122.0 160.2,129.0 153.8,129.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="313" y1="150" x2="313" y2="122" stroke-width="1.2" stroke="currentColor"/>
<polygon points="313.0,122.0 316.2,129.0 309.8,129.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="14" y="150" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">查 d</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">d 的三个位置：3、5、11</text>
<text x="8" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">c（从没加过）位 2、7、9 全是 1 → 误判</text>
<text x="8" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">d 的位 3 是 0 → 一定不存在</text>
</svg>
12 个位，3 个哈希；先加入了 a 和 b，亮起的位是 2、5、7、9、10。查 c：三个位置 2、7、9 全是 1，但 c 从没加过，这就是误判；查 d：位 3 是 0，一定不存在。
**容易错。**
- **以为能漏判：** 布隆过滤器不会漏判，只会误判；说「不存在」是绝对可靠的。
- **以为能直接删除元素：** 位被多个元素共用，清零会造成漏判；要删就换计数布隆（每位换成计数器，加 +1、删 −1）或布谷鸟过滤器（Cuckoo filter，存元素指纹，支持删除）。
- **把「可能存在」当成「一定存在」：** 要再查真实存储确认。
- **不规划容量：** 先定元素数 n 和可接受的误判率 p，位数 m = −n·ln p / (ln2)²，哈希个数 k = (m/n)·ln2；p=1% 约每元素 9.6 位、k≈7，p=0.1% 约 14.4 位、k≈10。装得比 n 多，误判率会快速上升。
- **不知道 Redis 怎么用：** Redis 8 内置，`BF.RESERVE ads 0.01 1000000`（误判率 1%、容量 100 万）建好后 `BF.ADD`、`BF.EXISTS`，实测约 1.38MB；更早版本装 RedisBloom 模块，Java 常用 Redisson 的 `RBloomFilter`。

**业务场景。** 百万广告里避免用户反复刷到已看过的广告：用布隆过滤器判断「可能看过」，占用极少内存；误判的后果只是少展示几条没看过的广告，可以接受。
