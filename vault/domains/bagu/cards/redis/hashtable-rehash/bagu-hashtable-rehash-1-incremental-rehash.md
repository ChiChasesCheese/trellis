---
id: bagu-hashtable-rehash-1-incremental-rehash
node: b.redis.hashtable-rehash
type: qa
step: 1
---
## Q
**Redis 哈希表 · 渐进式 rehash**｜追问

面试官：「Redis 的字典是怎么设计的？往里灌千万个 key 触发扩容，为什么主线程不会卡一整秒？」

## A
**基本回答。** 链地址法：同桶的冲突 key 挂链表。负载因子（键数 ÷ 桶数）达到 1 就扩成 2 倍；有 bgsave 子进程时为避免写时复制让内存暴涨，先推迟，涨到约 5 倍（7.4 起约 4 倍）才强制扩。不能一次搬完：主线程单线程，千万个 key 要整整一秒，所有请求排队。所以字典放两张表，平时只用第一张，扩容时建更大的第二张，`rehashidx` 记旧表搬到第几个桶，每次增删查顺带搬一个桶，旧表搬空后切换并释放。搬迁期间：查先旧表再新表；插入只写新表，旧表只减不增所以一定搬得完；删除和更新两张表都找。没有请求时搬迁会停在半路，所以定时任务每轮再搬约 1 毫秒（`activerehashing` 默认 yes）。代价是搬迁期间内存要同时容纳两张表，峰值更高。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 224">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ht[0] 旧表（4 个桶）</text>
<rect x="10" y="22" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="28" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已搬</text>
<rect x="50" y="22" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="68" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">已搬</text>
<rect x="90" y="22" width="36" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="108" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">待搬</text>
<rect x="130" y="22" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="148" y="39" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">待搬</text>
<line x1="108" y1="70" x2="108" y2="50" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="108,50 111.2,57 104.8,57" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="10" y="84" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">rehashidx = 2：下一个要搬的桶</text>
<line x1="290" y1="56" x2="290" y2="104" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="290,104 286.8,97 293.2,97" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="284" y="100" text-anchor="end" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">搬一个桶</text>
<text x="10" y="120" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">ht[1] 新表（8 个桶，旧表的 2 倍）</text>
<rect x="10" y="128" width="36" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="28" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="50" y="128" width="36" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="68" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="90" y="128" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="108" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="130" y="128" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="148" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="170" y="128" width="36" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="188" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="210" y="128" width="36" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="228" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="250" y="128" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="268" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="290" y="128" width="36" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="308" y="145" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">7</text>
<text x="10" y="178" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">查：先查旧表，再查新表</text>
<text x="10" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">插入：只写新表，旧表只减不增</text>
<text x="10" y="214" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">删除和更新：两张表都要找</text>
</svg>
旧表前两个桶已搬走，`rehashidx` 指着下一个；新表是旧表的 2 倍，每个旧桶 k 里的 key 只会落到新桶 k 或 k+4。
**业务场景。** 促销前一键灌入千万商品缓存，哈希表多次翻倍依然没有整秒卡顿：4 桶装 4 个 key，写第 5 个触发扩容建 8 桶新表，第 5 个 key 直接进新表，之后每次访问搬一桶；查一个没搬的 key 在旧表找到，搬走的在新表找到。
**容易错。**
- **以为扩容会暂停服务。**
- **以为搬迁期间能往旧表插入。**
- **以为有 bgsave 就永远不扩容。**
