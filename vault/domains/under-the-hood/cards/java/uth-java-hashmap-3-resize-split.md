---
id: uth-java-hashmap-3-resize-split
node: java.hashmap
type: qa
step: 3
---
## Q
**扩容时旧桶里的节点怎么分配**｜Java · OpenJDK 25

容量从 16 翻倍到 32，老桶 `j` 里的链表要重新计算每个节点的下标吗？

## A
**背景。** 元素太多时要扩容，所有节点都得放进新数组的合适位置。逐个重新算下标可以，但还能更省。

**结构。** 不用重算。新容量多出一位，节点只可能去两个位置：留在原下标 `j`，或移到 `j + oldCap`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="14" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧表 桶 5 的链</text>
<rect x="30" y="26" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="50" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<line x1="70" y1="39" x2="86" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,39.0 82.0,41.0 82.0,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="86" y="26" width="40" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="106" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<line x1="126" y1="39" x2="142" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="142.0,39.0 138.0,41.0 138.0,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="142" y="26" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="162" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<line x1="182" y1="39" x2="198" y2="39" stroke-width="1.2" stroke="currentColor"/>
<polygon points="198.0,39.0 194.0,41.0 194.0,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="198" y="26" width="40" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="218" y="43" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<line x1="120" y1="60" x2="120" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,84.0 117.0,78.0 123.0,78.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="132" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">一遍扫完 按 hash &amp; 16 分成两条</text>
<text x="14" y="108" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新表 桶 5</text>
<rect x="30" y="118" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="50" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="86" y="118" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="106" y="135" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<line x1="70" y1="131" x2="86" y2="131" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,131.0 82.0,133.0 82.0,129.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="150" y="136" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">hash &amp; 16 为 0 留在原桶</text>
<text x="14" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新表 桶 21</text>
<rect x="30" y="178" width="40" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="50" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="86" y="178" width="40" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="106" y="195" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d</text>
<line x1="70" y1="191" x2="86" y2="191" stroke-width="1.2" stroke="currentColor"/>
<polygon points="86.0,191.0 82.0,193.0 82.0,189.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="150" y="196" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">否则去 桶 5 + 16</text>
</svg>
```

**细节。**

- 判断式是 `(hash & oldCap) == 0`：为 0 留在低位桶，否则去高位桶。
- 一条链被拆成两条，各自保持原来的相对顺序，只遍历一遍。
- 红黑树桶用 `TreeNode.split` 同样拆分，拆出的节点数不超过 6 就退回链表。

**为什么。** 容量是 2 的幂，翻倍只相当于多看一位哈希，一次遍历就能拆成两条，不用逐个重新取模。

**对应 LeetCode：** 无直接对应的题
