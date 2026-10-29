---
id: uth-java-hashmap-2-spread
node: java.hashmap
type: qa
step: 2
---
## Q
**为什么哈希值要异或右移 16 位**｜Java · OpenJDK 25

`HashMap` 里 `hash(key)` 为什么是 `h ^ (h >>> 16)`，而不是直接用 `hashCode()`？

## A
**背景。** 桶下标只取哈希值的低几位（`& (n-1)`），高位完全用不上。如果一批 key 只有高位不同，它们会全挤进同一个桶。

**结构。** 扰动函数（spread）把高 16 位异或进低 16 位，让高位也参与桶的选择。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="10" y="44" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">h</text>
<rect x="70" y="26" width="120" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">高 16 位</text>
<rect x="190" y="26" width="120" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="250" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">低 16 位</text>
<text x="10" y="94" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">h &gt;&gt;&gt; 16</text>
<rect x="70" y="76" width="120" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">全 0</text>
<rect x="190" y="76" width="120" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">高 16 位</text>
<text x="10" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">异或后</text>
<rect x="70" y="126" width="120" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="143" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">高 16 位</text>
<rect x="190" y="126" width="120" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="250" y="143" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">低 异或 高</text>
<text x="250" y="172" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">桶下标 取最低几位</text>
</svg>
```

**细节。**

- 实测：容量 16 时，`hashCode` 为 `1<<16`、`2<<16` … `6<<16` 的 key，不扰动全落在桶 0；扰动后落在 1 到 6。
- 源码注释举的例子：小表里存连续整数的 `Float` 键，高位不同、低位相同。

**为什么。** 有红黑树兜底，不必用更贵的混合函数；一次异或就挽回大部分系统性冲突。

**对应 LeetCode：** 无直接对应的题
