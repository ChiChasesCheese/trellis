---
id: bagu-massive-data-topk-1-split-heap-bitmap
node: b.scenario.massive-data-topk
type: qa
step: 1
---
## Q
**海量数据 · Top K、去重与中位数**｜追问

面试官：「几十 TB 的用户 ID 日志，内存只有 4GB，怎么找出出现次数最多的 10 个？40 亿个 QQ 号怎么去重？」

## A
**基本回答。** 分治：`hash(id) % N` 把日志切到 N 个小文件，同一个 ID 不管出现多少次必落同一个文件，文件内数到的就是全局次数；每文件装得进内存，用哈希表计数，取本文件前 10 放进大小为 10 的小顶堆，各文件候选归并得全局前 10。不哈希随便切会错：x 共 6 次分散在 3 个文件各 2 次，y 3 次全在文件 1，局部冠军比出 y(3) 胜 x(2)，但全局是 x 最多。小顶堆求最大 K：堆顶是第 K 大，新数更大才替换，O(n log K)，内存只要 K 个元素；求最小 K 用大顶堆。N 按总量除以可用内存再留余量，30TB 按 1GB 一份要 3 万个文件，句柄太多就分两轮切；某文件仍太大说明某个 ID 太热，换哈希函数继续切。去重用位图：40 亿号在 32 位范围内，2^32 位 = 512MB，置位后顺序扫描；位图只记有没有、不记次数，内存仍不够就按数值区间分批或用布隆过滤器（允许误判）。中位数：放得下用大小两个堆；放不下就按高位分桶计数，一遍扫描定位中位数所在的桶，再细分该桶，每次只载一个桶。
**2026 亮点。** 数据是持续的流、要近实时时，改用 Count-Min Sketch 加堆。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 290">
<rect x="90" y="6" width="140" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="23.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">几十 TB 日志</text>
<text x="240" y="24" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">hash(id) % N</text>
<rect x="6" y="62" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="41.0" y="79.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">文件 0</text>
<line x1="160" y1="32" x2="41.0" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="41.0,60.0 47.1,55.3 48.5,61.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="104" width="70" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="41.0" y="121.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计数</text>
<text x="41.0" y="136.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取前 10</text>
<line x1="41.0" y1="88" x2="41.0" y2="102" stroke-width="1.2" stroke="currentColor"/>
<polygon points="41.0,102.0 37.8,95.0 44.2,95.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="41.0" y1="144" x2="170" y2="170" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,170.0 162.5,171.8 163.8,165.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="92" y="62" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="127.0" y="79.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">文件 1</text>
<line x1="160" y1="32" x2="127.0" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="127.0,60.0 130.3,53.0 134.4,57.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="92" y="104" width="70" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="127.0" y="121.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计数</text>
<text x="127.0" y="136.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取前 10</text>
<line x1="127.0" y1="88" x2="127.0" y2="102" stroke-width="1.2" stroke="currentColor"/>
<polygon points="127.0,102.0 123.8,95.0 130.2,95.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="127.0" y1="144" x2="170" y2="170" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,170.0 162.4,169.1 165.7,163.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="62" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="213.0" y="79.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">文件 2</text>
<line x1="160" y1="32" x2="213.0" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="213.0,60.0 205.3,59.6 208.3,53.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="178" y="104" width="70" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="213.0" y="121.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计数</text>
<text x="213.0" y="136.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取前 10</text>
<line x1="213.0" y1="88" x2="213.0" y2="102" stroke-width="1.2" stroke="currentColor"/>
<polygon points="213.0,102.0 209.8,95.0 216.2,95.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="213.0" y1="144" x2="170" y2="170" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,170.0 174.3,163.6 177.6,169.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="258" y="62" width="76" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="296.0" y="79.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">文件 N−1</text>
<line x1="160" y1="32" x2="296.0" y2="60" stroke-width="1.2" stroke="currentColor"/>
<polygon points="296.0,60.0 288.5,61.7 289.8,55.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="258" y="104" width="76" height="40" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="296.0" y="121.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">计数</text>
<text x="296.0" y="136.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">取前 10</text>
<line x1="296.0" y1="88" x2="296.0" y2="102" stroke-width="1.2" stroke="currentColor"/>
<polygon points="296.0,102.0 292.8,95.0 299.2,95.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="296.0" y1="144" x2="170" y2="170" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,170.0 176.2,165.5 177.5,171.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="70" y="172" width="200" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="191.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">候选归并 → 全局前 10</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">去重：位图 2^32 位 = 512MB</text>
<rect x="10" y="236" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="23.0" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="38" y="236" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="51.0" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="66" y="236" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="79.0" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="94" y="236" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="107.0" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="122" y="236" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="135.0" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="150" y="236" width="26" height="22" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="163.0" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="178" y="236" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="191.0" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="206" y="236" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="219.0" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="234" y="236" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="247.0" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="262" y="236" width="26" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275.0" y="251.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<text x="8" y="280" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">号 3、5 出现 → 对应位置 1；重复的号不变</text>
</svg>
上半部分：日志按 `hash(id) % N` 分到 N 个文件，文件内计数、取前 10，再归并成全局前 10。下半部分：位图每个号对应一个位，重复的号再置 1 没变化。
**举个例子。** 小顶堆求最大 3 个，依次来 5、1、9、3、7：前三个入堆 [1,5,9]；3 比堆顶 1 大，换成 [3,5,9]；7 比堆顶 3 大，换成 [5,7,9]。分桶求中位数：3、15、17、22、24、28、31、45、47、52 按十位分桶，0–9 有 1 个，10–19 有 2 个（累计 3），20–29 有 3 个（累计 6）；中位数是第 5、6 位，落在 20–29 桶，再看桶内第 2、3 个得 24 和 28。
**业务场景。** 风控找昨天请求打赏接口最多的前 10 个 IP，日志几十 TB：按 IP 哈希分桶、桶内计数、小顶堆归并。
**容易错。**
- **求最大 K 用大顶堆：** 要用小顶堆。
- **以为位图能数次数：** 要次数得用哈希表分治。
