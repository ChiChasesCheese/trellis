---
id: tr-test-infra-sharding-bin-packing
node: test-infra.sharding
type: qa
step: 1
---
## Q
把一个测试套件切成 N 个分片（shard）并行跑，为什么要按历史耗时分，而不是按测试个数平均分？按耗时分的算法是什么？用一个小例子算一遍。

## A
**总时长由最慢的那个分片决定**，所以目标是让各分片耗时尽量相等，而不是个数相等。

**按个数平均分的问题**：8 条测试分 2 片，每片 4 条。如果一个分片里碰巧有两条 20 分钟的长测试，它要 45 分钟，另一片 10 分钟，并行几乎没起作用。

**按耗时分：最长优先贪心（LPT，longest processing time first）**：
1. 从结果库取每条测试最近若干次的耗时（中位数）；
2. 按耗时从长到短排序；
3. 依次把每条测试放进当前总耗时最小的分片。

例：6 条测试耗时（分钟）为 20、15、10、8、5、2，分 3 片。

| 放入 | 分片 A | 分片 B | 分片 C |
|---|---|---|---|
| 20 → A | 20 | 0 | 0 |
| 15 → B | 20 | 15 | 0 |
| 10 → C | 20 | 15 | 10 |
| 8 → C | 20 | 15 | 18 |
| 5 → B | 20 | 20 | 18 |
| 2 → C | 20 | 20 | 20 |

总时长 20 分钟，等于最长那条测试，已是下限。按原顺序轮流分（20、8 进 A，15、5 进 B，10、2 进 C）则是 28、20、12，总时长 28 分钟。

两种分法的分片耗时（分钟，虚线是 20 分钟下限）：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<g font-family="sans-serif" font-size="12" fill="currentColor">
<path fill-opacity="0.12" stroke="currentColor" stroke-width="0.8" d="M40,26h180v20h-180zM40,50h135v20h-135zM175,50h45v20h-45zM40,74h90v20h-90zM130,74h72v20h-72zM202,74h18v20h-18zM40,126h180v20h-180zM220,126h72v20h-72zM40,150h135v20h-135zM175,150h45v20h-45zM40,174h90v20h-90zM130,174h18v20h-18z"/>
<path fill="none" stroke="currentColor" stroke-dasharray="4 3" d="M220,22V192"/>
<text x="10" y="18">LPT 最长优先</text>
<text x="22" y="41">A</text>
<text x="130.0" y="40" text-anchor="middle">20</text>
<text x="22" y="65">B</text>
<text x="107.5" y="64" text-anchor="middle">15</text>
<text x="197.5" y="64" text-anchor="middle">5</text>
<text x="22" y="89">C</text>
<text x="85.0" y="88" text-anchor="middle">10</text>
<text x="166.0" y="88" text-anchor="middle">8</text>
<text x="211.0" y="88" text-anchor="middle">2</text>
<text x="330" y="90" text-anchor="end">总时长20</text>
<text x="10" y="118">按原顺序轮流分</text>
<text x="22" y="141">A</text>
<text x="130.0" y="140" text-anchor="middle">20</text>
<text x="256.0" y="140" text-anchor="middle">8</text>
<text x="22" y="165">B</text>
<text x="107.5" y="164" text-anchor="middle">15</text>
<text x="197.5" y="164" text-anchor="middle">5</text>
<text x="22" y="189">C</text>
<text x="85.0" y="188" text-anchor="middle">10</text>
<text x="139.0" y="188" text-anchor="middle">2</text>
<text x="330" y="190" text-anchor="end">总时长28</text>
</g>
</svg>
```

**两个下限**：总时长 ≥ 总耗时 ÷ 分片数（这里 60 ÷ 3 = 20），也 ≥ 最长的单条测试。要突破第二个下限只能拆那条测试本身。

**没有历史数据的新测试**：先给一个默认估计（例如同目录测试的中位数），跑一次后用真实值。
