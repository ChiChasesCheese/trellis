---
id: uth-gaps-intervals-2-gist
node: gaps.intervals
type: qa
step: 2
---
## Q
**查重叠为什么不用扫全表**｜PostgreSQL · 17 GiST 索引

表里有几百万条预订，插入一条新的时，数据库怎样不扫全表就找出和它重叠的行？

## A
**背景。** 只按开始时间排序的 B 树（B-tree）帮不上忙：开始早于新预订结束的行可能占大半张表，其中结束晚于新预订开始的才算重叠，只能逐行查。

**结构。** GiST（通用搜索树，Generalized Search Tree）是平衡树。叶子存每行的范围，上层每个条目存「盖住下面所有范围的最小范围」。先问上层：你盖住的范围和我重叠吗？不重叠，整棵子树跳过。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 170">
<text x="170" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">查询 [15,16)</text>
<rect x="28" y="28" width="80" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="68" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">[9,13)</text>
<rect x="200" y="28" width="80" height="26" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="240" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">[14,20)</text>
<line x1="68" y1="54" x2="36" y2="110" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<rect x="11" y="110" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="36" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">[9,11)</text>
<line x1="68" y1="54" x2="100" y2="110" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<rect x="75" y="110" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" opacity="0.45"/>
<text x="100" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">[10,13)</text>
<line x1="240" y1="54" x2="180" y2="110" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="155" y="110" width="50" height="26" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="180" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">[14,16)</text>
<line x1="240" y1="54" x2="240" y2="110" fill="none" stroke="currentColor" stroke-width="1.8" style="stroke:var(--accent,#3b6fd4)"/>
<rect x="215" y="110" width="50" height="26" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="240" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">[15,17)</text>
<line x1="240" y1="54" x2="300" y2="110" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="275" y="110" width="50" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="300" y="127" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">[18,20)</text>
<text x="68" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">不重叠 整棵跳过</text>
<text x="240" y="158" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">重叠 往下查</text>
</svg>
```

**细节。**

- 上层只回答「可能有」，叶子才精确比较
- 新范围放进哪个分支，由 penalty（代价）函数挑；放得散，上层范围就宽，剪枝变少

**为什么。** GiST 把「怎样盖住、怎样算相近」交给数据类型，同一套树能索引范围、几何框等；B 树只认大小顺序。

**对应 LeetCode：** 无直接对应的题
