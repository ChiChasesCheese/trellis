---
id: hi-sdx-docs-format-span-anchor
node: sd.problem-breakdowns.google-docs.more
type: qa
step: 1
---
## Q
**富文本格式要锚在字符 ID 上**｜补充 · 协同文档（Google Docs） · 加分

面试官：「协同编辑器里用户选中一段文字加粗。你把加粗记成『从第 5 个字符到第 12 个字符』吗？别人同时在前面插入文字，这个范围会怎样？在加粗段的末尾继续打字，新字符该不该加粗？」

## A
**结论。** 不用数字偏移，把格式跨度的起点和终点锚在首尾字符各自的稳定 ID 上。并发的插入和删除只会让端点移动或收缩，跨度不会错位；每种格式再声明自己在边界处是否向外延伸。

**要点。**
- **偏移会失效：** 别人在前面插一个字符，所有数字位置整体后移一位，加粗范围就套到了错的字符上。
- **锚在字符 ID 上：** 跨度记成 (起点字符 ID, 终点字符 ID, 格式)，字符被插入或删除时，范围跟着字符走，不需要改写。
- **边界行为按类型声明：** 加粗、斜体在末尾继续输入时延伸；链接、评论批注不吸收边界处的新输入。
- **同位置并发插入：** 两人同时在同一点各输入一段，合并算法要保持每人的内容连在一起，不能逐字符交错。
- **删除端点的字符：** 墓碑仍保留 ID，所以跨度的锚点依然存在，不会悬空。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 250">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">加粗从 id2 到 id4，锚在字符 ID 上</text>
<rect x="10" y="26" width="46" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="33.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">H</text>
<text x="33.0" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id1</text>
<rect x="62" y="26" width="46" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<text x="85.0" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id2</text>
<rect x="114" y="26" width="46" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="137.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<text x="137.0" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id3</text>
<rect x="166" y="26" width="46" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="189.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<text x="189.0" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id4</text>
<rect x="218" y="26" width="46" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="241.0" y="39.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">o</text>
<text x="241.0" y="54.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id5</text>
<line x1="62" y1="70" x2="212" y2="70" stroke-width="1" stroke="currentColor" opacity="0.4"/>
<text x="10" y="92" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">别人在最前面插入 X（offset 全部后移）</text>
<rect x="10" y="102" width="48" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="34.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">X</text>
<text x="34.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id9</text>
<rect x="63" y="102" width="48" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="87.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">H</text>
<text x="87.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id1</text>
<rect x="116" y="102" width="48" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="140.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e</text>
<text x="140.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id2</text>
<rect x="169" y="102" width="48" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="193.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<text x="193.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id3</text>
<rect x="222" y="102" width="48" height="34" rx="6" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="246.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">l</text>
<text x="246.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id4</text>
<rect x="275" y="102" width="48" height="34" rx="6" stroke-width="1.2" fill="none" stroke="currentColor"/>
<text x="299.0" y="115.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">o</text>
<text x="299.0" y="130.5" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">id5</text>
<line x1="116" y1="146" x2="270" y2="146" stroke-width="1" stroke="currentColor" opacity="0.4"/>
<text x="10" y="176" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">跨度端点跟着字符走，不用改数字</text>
<text x="10" y="198" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">末端：加粗继续向外延伸（grow）</text>
<text x="10" y="216" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">链接、评论：不吸收边界处的新输入</text>
<text x="10" y="234" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每种格式自己声明边界行为</text>
</svg>

**为什么。** 数字位置是相对某一版文档的坐标，并发编辑下坐标不稳定；字符 ID 是文档的身份，不随别人的编辑变化。

**面试里这样说。** 「我把格式记成一对字符 ID 加类型，不记数字偏移，别人并发插入只移动端点，不会让加粗套错字。每种格式自己声明边界是否延伸：加粗延伸，链接不延伸，这样在链接末尾继续打字不会把新字也变成链接。」

**易错。**
- **用偏移存格式：** 并发编辑后范围错位，需要对每个范围反复重算。
- **所有格式统一向外延伸：** 链接、评论会吞掉边界处的新文字。
- **删除端点字符后丢弃跨度：** 应保留墓碑作为锚点，或明确把端点收缩到相邻字符。
