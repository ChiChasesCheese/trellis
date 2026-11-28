---
id: bagu-encodings-1-object-encoding
node: b.redis.encodings
type: qa
step: 1
---
## Q
**五种基本类型 · 底层编码与升级**｜追问

面试官：「Redis 的 String、List、Hash、Set、ZSet 底层分别用什么编码？什么时候会换，换了对线上有什么影响？」

## A
**基本回答。** 小数据用连续内存（省指针和哈希开销、遍历对 CPU 缓存友好），大了才换指针结构。String：能当整数用 int，短字符串 embstr（对象头和字符串同一块内存，值长上限 44 字节；8.2 起 key 也嵌进同块，整块超过 64 字节退回 raw，以 `OBJECT ENCODING` 为准），其余 raw（SDS：自带长度 O(1)、二进制安全、写前检查空间，单值上限 512MB）。List：quicklist（3.2 起），节点里的紧凑内存 7.0 起从 ziplist 换成 listpack。Hash、ZSet 少时 listpack，超阈值换 hashtable、skiplist 加 dict（dict 管 member 到 score 的 O(1)，跳表管排序和范围）。Set 全整数用 intset。默认阈值：Hash 512 字段且值不超过 64 字节；ZSet 128 个且值不超过 64 字节；Set 的 intset 最多 512 个整数，listpack（7.2 起）128 个且不超过 64 字节；个数或单值任一超了就换。换编码单向：成了 hashtable，元素删光也不退回。排查用 `OBJECT ENCODING key`、`MEMORY USAGE key`。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 228">
<text x="6" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">类型</text>
<text x="124" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">数据少：连续内存</text>
<text x="273" y="14" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">超阈值：指针结构</text>
<rect x="6" y="24" width="54" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="33" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">String</text>
<rect x="68" y="24" width="112" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">int / embstr</text>
<line x1="182" y1="37" x2="210" y2="37" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210,37 203,40.2 203,33.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="212" y="24" width="122" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">raw（SDS）</text>
<rect x="6" y="56" width="54" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="33" y="73" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">List</text>
<rect x="68" y="56" width="266" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="201" y="73" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">quicklist：链表，每节点一段 listpack</text>
<rect x="6" y="88" width="54" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="33" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Hash</text>
<rect x="68" y="88" width="112" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">listpack</text>
<line x1="182" y1="101" x2="210" y2="101" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210,101 203,104.2 203,97.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="212" y="88" width="122" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="273" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">hashtable</text>
<rect x="6" y="120" width="54" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="33" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Set</text>
<rect x="68" y="120" width="112" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">intset</text>
<line x1="182" y1="133" x2="210" y2="133" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210,133 203,136.2 203,129.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="212" y="120" width="122" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273" y="137" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">hashtable</text>
<rect x="6" y="152" width="54" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="33" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ZSet</text>
<rect x="68" y="152" width="112" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="124" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">listpack</text>
<line x1="182" y1="165" x2="210" y2="165" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="210,165 203,168.2 203,161.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="212" y="152" width="122" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="273" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">skiplist + dict</text>
<text x="6" y="200" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">Hash 默认 512 字段或值 &gt;64 字节就换</text>
<text x="6" y="218" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">换了就不退回，元素删光也一样</text>
</svg>
左边是数据少时的编码，右边是超阈值后的编码；List 一直是 quicklist。
**业务场景。** 用户标签集合 500 个整数是 intset，占 2028 字节；运营写进一个字符串标签，编码悄悄变成 hashtable，占 16193 字节，约 8 倍；之后把字符串和多余元素删光，也不会退回。
**容易错。**
- **以为只看元素个数：** 单个值大小和类型也触发。
- **以为元素删光会退回。**
- **以为 embstr 边界到处是 44。**
