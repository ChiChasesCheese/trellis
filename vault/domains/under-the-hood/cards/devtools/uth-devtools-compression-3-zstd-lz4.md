---
id: uth-devtools-compression-3-zstd-lz4
node: devtools.compression
type: qa
step: 3
---
## Q
**LZ4 为什么解压那么快**｜LZ4 · 1.10 与 zstd · 1.5.7

只要速度时，压缩可以做到多简单？zstd 在它的基础上多做了什么？

## A
**背景。** LZ77 之后再做哈夫曼（DEFLATE 的做法），压得小，但解压要一位一位地解码。如果只要速度，可以只做 LZ77，把结果用最简单的字节格式存下来：LZ4 就是这样。

**结构。** LZ4 的压缩块由若干“序列”组成，每个序列是：1 字节 token（高 4 位是后面原样字节的个数，低 4 位是匹配长度减 4）、原样字节（字面量）、2 字节偏移（往回多远）。例（示意）：`abcabcabc` 写成 token 3|2，原样 `abc`，偏移 3；解压时先抄出 `abc`，再往回 3 个、复制 4+2 = 6 个字节。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 196">
<text x="60" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">token</text>
<text x="142" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">原样字节</text>
<text x="229" y="20" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">偏移</text>
<rect x="30" y="28" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<text x="60" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3 | 2</text>
<rect x="100" y="28" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="114" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a</text>
<rect x="128" y="28" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="142" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b</text>
<rect x="156" y="28" width="28" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c</text>
<rect x="194" y="28" width="70" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="229" y="47" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">3</text>
<text x="60" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">原样 3 个</text>
<text x="60" y="90" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">匹配 4+2</text>
<text x="229" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">往回 3 个</text>
<line x1="170" y1="100" x2="170" y2="113" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<path d="M170.0,118.0 L166.7,111.2 L173.3,111.2 Z" stroke="none" style="fill:var(--accent,#3b6fd4)"/>
<rect x="44" y="122" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="58" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a</text>
<rect x="72" y="122" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="86" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b</text>
<rect x="100" y="122" width="28" height="28" rx="2" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="114" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c</text>
<rect x="128" y="122" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="142" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a</text>
<rect x="156" y="122" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b</text>
<rect x="184" y="122" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="198" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c</text>
<rect x="212" y="122" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="226" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a</text>
<rect x="240" y="122" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="254" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b</text>
<rect x="268" y="122" width="28" height="28" rx="2" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="282" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">先抄 abc 再往回 3 个复制 6 个</text>
<text x="170" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">解压只有读 抄 复制 三步</text>
</svg>
```

**细节。**

- 偏移最大 65535（窗口 64 KB），最短匹配 4 字节；长度字段填满 15 时，后面的字节继续累加
- 解压只是读 token、拷贝字面量、按偏移复制，没有位级解码
- zstd 在 LZ 之上再按出现频率做编码（字面量用哈夫曼，序列用更精细的 FSE），窗口也大得多：解码器至少要支持 8 MB 窗口，DEFLATE 只有 32 KB

**为什么。** LZ4 用压缩率换速度；zstd 补上频率编码，窗口也更大，所以压得更小。

**对应 LeetCode：** 无直接对应的题
