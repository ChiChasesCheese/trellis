---
id: uth-devtools-compression-2-huffman
node: devtools.compression
type: qa
step: 2
---
## Q
**哈夫曼编码：常见的字母用短码**｜DEFLATE · 哈夫曼

一段文字里 `a` 出现最多、`d` 最少，怎样给常见字符更短的编码？DEFLATE 又怎样把码表告诉解压方？

## A
**背景。** 4 个字母要区分开，固定每个用 2 位。可如果 `a` 出现 5 次、`b` 2 次、`c` 和 `d` 各 1 次，给常见的 a 一个短码、罕见的 c、d 长码，总位数更少。变长码有个麻烦：码连在一起怎么拆？要求没有哪个码是另一个码的开头（前缀码），读到一个完整的码就能立刻断开。

**结构。** 哈夫曼编码：把符号按频率放进最小堆（总能取出最小元素的结构），反复弹出最小的两个合并成新节点，直到只剩一棵树；从根往下，左走 0、右走 1，路径就是编码，高频符号离根近。例：c+d 合成 2，再与 b 合成 4，再与 a 合成 9；码为 a=0、b=10、c=110、d=111，共 5×1 + 2×2 + 1×3 + 1×3 = 15 位，比固定 2 位的 18 位少。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 236">
<circle cx="170" cy="26" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="30" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">9</text>
<rect x="90" y="68" width="40" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="110" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a 5</text>
<circle cx="230" cy="80" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="230" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">4</text>
<rect x="170" y="122" width="40" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="190" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b 2</text>
<circle cx="270" cy="134" r="14" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="270" y="138" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">2</text>
<rect x="220" y="178" width="40" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="240" y="194" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c 1</text>
<rect x="280" y="178" width="40" height="24" rx="3" stroke="currentColor" stroke-width="1.8" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="300" y="194" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">d 1</text>
<line x1="160" y1="37" x2="118" y2="68" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="180" y1="37" x2="222" y2="68" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="222" y1="91" x2="194" y2="122" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="238" y1="91" x2="262" y2="122" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="262" y1="145" x2="244" y2="178" fill="none" stroke="currentColor" stroke-width="1.2"/>
<line x1="278" y1="145" x2="296" y2="178" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="132" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">0</text>
<text x="208" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="196" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">0</text>
<text x="254" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="246" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">0</text>
<text x="296" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--accent,#3b6fd4)">1</text>
<text x="14" y="100" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">编码</text>
<text x="14" y="120" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">a = 0</text>
<text x="14" y="138" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">b = 10</text>
<text x="14" y="156" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">c = 110</text>
<text x="14" y="174" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none">d = 111</text>
<text x="170" y="228" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor" stroke="none" style="fill:var(--dim,#6b7280)">每次合并最小的两个 高频离根近</text>
</svg>
```

**细节。**

- DEFLATE 不传整棵树，只传每个符号的码长（0 到 15），双方按同一规则重建码表：短码在前，同长度的码按符号顺序连续排列（规范哈夫曼，canonical Huffman）
- 因此码表几乎不占空间

**为什么。** 贪心地合并最小的两个，得到的就是最优前缀码；只传码长，让码表几乎免费。

**例题：** LC 1167 连接木棍的最低费用

每次取两根长度为 x、y 的木棍连成长度 x + y 的新木棍，代价也是 x + y，重复到只剩一根，求最小总代价。`1 <= sticks.length <= 10^4`。例：`[2,4,3]` → 14。

```python
import heapq

def connect_sticks(sticks: list[int]) -> int:
    heapq.heapify(sticks)
    cost = 0
    while len(sticks) > 1:
        merged = heapq.heappop(sticks) + heapq.heappop(sticks)
        cost += merged
        heapq.heappush(sticks, merged)
    return cost
```
