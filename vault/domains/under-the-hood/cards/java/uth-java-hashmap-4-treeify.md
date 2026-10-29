---
id: uth-java-hashmap-4-treeify
node: java.hashmap
type: qa
step: 4
---
## Q
**链表长到 8 一定转红黑树吗**｜Java · OpenJDK 25

同一个桶里的链表长度达到 8 时，`HashMap` 会马上转成红黑树吗？

## A
**背景。** 同一个桶里的链表太长，查找就退化成 O(n)。红黑树（一种自动保持平衡的二叉查找树）最坏 O(log n)，但树节点比普通节点大得多，只该给冲突严重的桶用。

**结构。** 不一定马上转。转树要同时满足链长够长（`TREEIFY_THRESHOLD = 8`）和表长至少 64（`MIN_TREEIFY_CAPACITY`）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<rect x="90" y="14" width="160" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="32" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">链表长度达到 8</text>
<line x1="170" y1="42" x2="170" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170.0,64.0 167.0,58.0 173.0,58.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="90" y="64" width="160" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">表长 &gt;= 64 ?</text>
<line x1="130" y1="92" x2="90" y2="124" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,124.0 92.8,117.9 96.6,122.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="210" y1="92" x2="250" y2="124" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="250.0,124.0 243.4,122.6 247.2,117.9" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="98" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">否</text>
<text x="252" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">是</text>
<rect x="14" y="124" width="140" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="84" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">resize 扩容</text>
<text x="84" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">把冲突摊开</text>
<rect x="186" y="124" width="140" height="52" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="256" y="146" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">转成红黑树</text>
<text x="256" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">树节点约 2 倍大</text>
</svg>
```

**细节。**

- 表长不足 64 时，链表过长只触发 `resize()`，把冲突摊开。
- 实测 11 个哈希全相同的 key：第 9 次插入表长 16→32，第 10 次 32→64，第 11 次才变 `TreeNode`。

**为什么。** 树节点约是普通节点的两倍大。树先按哈希排序，哈希相同再比 `Comparable`，最坏 O(log n)。

**坑。** 键没有实现 `Comparable` 且哈希全相同时，查找仍会退化为线性。

**对应 LeetCode：** 无直接对应的题
