---
id: uth-go-rust-modern-sorts-3-sorted-input
node: go-rust.modern-sorts
type: qa
step: 3
---
## Q
**对已经有序的数据排序有多快**｜Go / Rust · 现代标准库

给 100 万个已经升序或逆序的整数排序，要比较多少次？

## A
**背景。** 排序一个本来就排好的数组，理想情况只需看一遍确认“没问题”。老式快排不会这么想，枢轴选不好时对有序输入可能退化到 O(n²)；现代标准库先检测，再走快路径。

**结构。** pdqsort、driftsort、ipnsort 都先检测“输入已有序”，直接走 O(n) 的快路径。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 185">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">已升序的输入: 只扫一趟, 比较 n - 1 次</text>
<rect x="10" y="26" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="30" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="57" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≤</text>
<rect x="64" y="26" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="84" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="111" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≤</text>
<rect x="118" y="26" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="138" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="165" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≤</text>
<rect x="172" y="26" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="192" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<text x="219" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≤</text>
<rect x="226" y="26" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="246" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<text x="273" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">≤</text>
<rect x="280" y="26" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="300" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<text x="8" y="96" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">已逆序的输入: 同样扫一趟, 发现全是降序</text>
<rect x="10" y="108" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="30" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">6</text>
<rect x="64" y="108" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="84" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="118" y="108" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="138" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">4</text>
<rect x="172" y="108" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="192" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="226" y="108" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="246" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="280" y="108" width="40" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="300" y="124.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<text x="8" y="160" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">整体反转一遍, 就变成有序, 总共仍是 O(n)</text>
<text x="8" y="178" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">老式快排对有序输入可能退化到 O(n²)</text>
</svg>
```

**细节。**

- Rust 实测：升序、逆序的 `sort_by` 与 `sort_unstable_by` 都恰好 999999 次，即 n-1
- Go 实测：`sort.Slice` 升序、逆序都约 1000011 次
- Go 遇到逆序会先整体反转，再按有序处理

**为什么。** 检测只要扫一趟，却把常见的“已排好”场景降到线性；老式快排对有序输入可能退化到 O(n²)。

**坑。** Rust 1.81 起，比较函数不满足全序（total order：任意两个元素都能比出大小，且不自相矛盾）时，排序可能直接 panic，而不是悄悄返回乱序结果。

**对应 LeetCode：** 无直接对应的题（标准库的输入检测）
