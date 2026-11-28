---
id: bagu-bplus-tree-3-capacity
node: a.mysql.bplus-tree
type: qa
step: 3
---
## Q
**三层 B+ 树能存多少行，数字怎么算**｜必会

面试官：「三层的 B+ 树大概能存多少行？『单表超过两千万行要分表』这个说法怎么来的？」

## A
**基本回答。** 非叶子页每页约 1170 个指针；叶子页存整行，设每行约 1KB，一页放 16 行。三层 B+ 树就是：1 个根页 → 1170 个第二层页 → 每个第二层页再指向 1170 个叶子页，总行数 1170 × 1170 × 16 ≈ 2190 万；四层约 256 亿。「单表不超过两千万」就是行长约 1KB 时三层树的容量，意思是再涨就多一层、多一次页访问，不是硬上限。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<rect x="110" y="8" width="120" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="25.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">根页 1 页</text>
<line x1="170" y1="34" x2="170.0" y2="49.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,56.0 166.8,49.0 173.2,49.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="50" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">×1170</text>
<rect x="60" y="56" width="220" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="73.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">第二层 1170 页</text>
<line x1="170" y1="82" x2="170.0" y2="97.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,104.0 166.8,97.0 173.2,97.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="98" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">×1170</text>
<rect x="8" y="104" width="324" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170.0" y="121.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">叶子层 1170×1170 ≈ 137 万页</text>
<line x1="170" y1="130" x2="170.0" y2="145.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,152.0 166.8,145.0 173.2,145.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="178" y="146" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">×16 行/页</text>
<rect x="8" y="152" width="324" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="169.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">约 2190 万行（行长 1KB）</text>
<text x="8" y="202" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">每加一层容量×1000，多 1 次页访问</text>
<text x="8" y="222" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">根页和第二层（约 18MB）常驻内存</text>
</svg>
自上而下：1 个根页，每页展开成 1170 个子页，到叶子层约 137 万页，每页 16 行，总共约 2190 万行；每多一层容量乘约 1000，代价是多一次页访问。
**举个例子。** 用 1170 和每页 16 行，一步步算：
1. **第一层：** 1 个根页，里面 1170 个指针。
2. **第二层：** 1170 个页，每个页里又有 1170 个指针。
3. **叶子层：** 1170 × 1170 = 136.89 万个叶子页（约 137 万）。
4. **行数：** 136.89 万 × 16 行 ≈ 2190 万行，这就是「两千万」的来历。
5. **四层：** 再乘 1170，约 256 亿行。
6. **换成实测的 893：** 893 × 893 × 16 ≈ 1275 万，比教科书的数字小不少；若行只有 270 字节，每页 56 行，则约 4465 万。
**容易错。**
- **把两千万当成硬上限：** 它只是一个估算值，换行长、换索引大小结果就变；超过它也不会突然变慢。
- **以为四层一定很慢：** 根页和第二层都在内存里，四层和三层的差别只是多读一页。
- **只看行数不看行长：** 同样一亿行，行长 200 字节和 1KB 的树高不一样。
- **忘了索引能否放进内存：** 真正拖慢查询的是索引大到装不进缓冲池，不是层数本身。
