---
id: uth-storage-bloom-1-skip-file
node: storage.bloom
type: qa
step: 1
---
## Q
**布隆过滤器：这个文件里肯定没有**｜RocksDB · v10.9

按 key 读取时，同一个 key 可能出现在每一层的文件里。怎样不逐个读磁盘，就知道“这个文件里没有它”？

## A
**背景。** RocksDB 把数据存成多层有序的磁盘文件（SST，写好就不再修改）。查一个 key 要从新到旧一个文件一个文件地问；要查的 key 根本不存在时，每个文件都白读一次磁盘。把所有 key 放进内存来查，又太占地方。

**结构。** 布隆过滤器（Bloom filter）给每个 SST 配一个很小的内存结构：一个位数组加 k 个哈希函数。加入 key：算出 k 个位置，全部置 1。查询：算同样的 k 个位置，只要有一位是 0，这个 key 就一定不在；全是 1 才是“可能在”。图里 a、b 写入之后，c 的第三个位置是 0，这个文件就不用读了。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 108">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">写入 a, b 之后的位数组 (k = 3)</text>
<rect x="26" y="22" width="18" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="35" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="44" y="22" width="18" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="53" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="62" y="22" width="18" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="80" y="22" width="18" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="89" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="98" y="22" width="18" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="107" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="116" y="22" width="18" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="125" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="134" y="22" width="18" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="143" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="152" y="22" width="18" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="161" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="170" y="22" width="18" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="179" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="188" y="22" width="18" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="197" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="206" y="22" width="18" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="215" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="224" y="22" width="18" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="233" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="242" y="22" width="18" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="260" y="22" width="18" height="22" fill="none" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="269" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="278" y="22" width="18" height="22" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="287" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="296" y="22" width="18" height="22" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="305" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<line x1="53" y1="64" x2="53" y2="52" stroke="currentColor" stroke-width="1.2"/>
<polygon points="53,46 56.0,52.0 50.0,52.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="143" y1="64" x2="143" y2="52" stroke="currentColor" stroke-width="1.2"/>
<polygon points="143,46 146.0,52.0 140.0,52.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="269" y1="64" x2="269" y2="52" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="269,46 272.0,52.0 266.0,52.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="80" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">查 c: 它的 3 个位置是 1 1 0</text>
<text x="170" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">有一位是 0: 一定不在, 不用读这个文件</text>
</svg>
```

**细节。**

- 每个 key 约 9.9 位，误判率约 1%（RocksDB 文档）。
- 误判只会多读一个文件，不会漏数据。
- 默认没开：`filter_policy` 默认是 `nullptr`，要自己配 `NewBloomFilterPolicy(10)`。

**为什么。** 位数组约 1.25 字节/key，常驻内存，换掉一次磁盘 I/O。

**坑。** 不支持删除：同一位可能被多个 key 共用。

**对应 LeetCode：** 无直接对应的题
