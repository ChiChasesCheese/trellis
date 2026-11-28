---
id: bagu-bplus-tree-2-bplus-vs-b
node: a.mysql.bplus-tree
type: qa
step: 2
---
## Q
**B+ 树和 B 树的区别，一个页能放多少个指针**｜必会

面试官：「B+ 树和 B 树差在哪？InnoDB 一个非叶子页能放多少个指针，怎么算？」

## A
**基本回答。** 差四点：B 树所有节点都存数据，B+ 树只有叶子存；所以 B+ 树非叶子扇出更大、树更矮；B+ 树查询一定走到叶子，IO 次数稳定；叶子之间有双向链表，范围查询找到起点后顺着走。估算一页能放多少指针：页 16KB，bigint 键 8 字节加指针按 6 字节，每条约 14 字节，一页约 16384 ÷ 14 ≈ 1170 个指针。
实测（MySQL 8.0，100 万行、行长约 270 字节）：叶子页 17858 个、每页平均 56 行；第一层非叶子页 20 个、每页平均 893 条；根 1 页，共 3 层。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">B 树：每个节点都存数据</text>
<rect x="48" y="24" width="84" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="90.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">键+数据</text>
<rect x="8" y="76" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44.0" y="93.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">键+数据</text>
<rect x="100" y="76" width="72" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="136.0" y="93.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">键+数据</text>
<line x1="75" y1="50" x2="51.211986084525435" y2="71.32718488973582" stroke-width="1.2" stroke="currentColor"/>
<polygon points="46.0,76.0 49.1,68.9 53.3,73.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="105" y1="50" x2="128.78801391547458" y2="71.32718488973582" stroke-width="1.2" stroke="currentColor"/>
<polygon points="134.0,76.0 126.7,73.7 130.9,68.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">B+ 树：只有叶子存数据</text>
<rect x="222" y="24" width="84" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="264.0" y="41.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">键+指针</text>
<rect x="186" y="76" width="64" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="218.0" y="93.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据</text>
<rect x="268" y="76" width="64" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="300.0" y="93.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">数据</text>
<line x1="256" y1="50" x2="225.67475459879915" y2="71.9015661230895" stroke-width="1.2" stroke="currentColor"/>
<polygon points="220.0,76.0 223.8,69.3 227.5,74.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="272" y1="50" x2="294.8704455586159" y2="71.23684230442906" stroke-width="1.2" stroke="currentColor"/>
<polygon points="300.0,76.0 292.7,73.6 297.0,68.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="250" y1="86" x2="261.0" y2="86.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="268.0,86.0 261.0,89.2 261.0,82.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="268" y1="94" x2="257.0" y2="94.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="250.0,94.0 257.0,90.8 257.0,97.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="126" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">非叶子页不存数据，一页能放更多指针：</text>
<rect x="8" y="134" width="324" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="151.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">一个 16KB 的非叶子页（16384 字节）</text>
<rect x="8" y="170" width="76" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="46.0" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">键 8B</text>
<text x="46.0" y="198.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">指针 6B</text>
<rect x="92" y="170" width="76" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="130.0" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">键 8B</text>
<text x="130.0" y="198.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">指针 6B</text>
<rect x="176" y="170" width="76" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="214.0" y="183.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">键 8B</text>
<text x="214.0" y="198.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">指针 6B</text>
<text x="292" y="191" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">……</text>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每条约 14B，16384÷14≈1170 个指针</text>
</svg>
上半部分对比两种树的节点内容：B 树每个节点都是「键 + 数据」，B+ 树的非叶子只有「键 + 指针」，数据只在叶子，叶子之间还有双向箭头；下半部分把一个 16KB 的非叶子页切成一条条「键 8B + 指针 6B」，数出约 1170 条。
**举个例子。** 拿那张 100 万行的表数一遍：
1. **根页：** 1 页，里面有约 20 个指针，指向第一层非叶子页。
2. **第一层非叶子页：** 20 个，每页平均 893 条指针，20 × 893 ≈ 17860，正好对上叶子页数量。
3. **叶子页：** 17858 个，每页平均 56 行，17858 × 56 ≈ 100 万行。
4. **3 层结构：** 根 → 第一层 → 叶子，查任何一行都是三页。
5. **换成 UUID 主键：** 36 个字符 + 页号和记录头，非叶子记录约 45 字节，一页只放 360 个左右，同样数据要的页更多、树更高。
**容易错。**
- **以为 B+ 树更快是因为比较少：** 比较次数差不多，赢在一页能放更多键，层数更少。
- **以为 1170 是精确值：** 它是 8 字节键 + 6 字节指针的教科书估算，实际约 900。
- **以为 B 树的范围查询也方便：** B 树的数据散在各层，范围扫描要在树里来回走；B+ 树叶子有链表，顺着读就行。
- **忘了二级索引也受主键影响：** 二级索引叶子里存的是主键值，主键越长，所有二级索引越大。
