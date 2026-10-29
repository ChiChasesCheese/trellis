---
id: uth-redis-zset-3-why-skiplist
node: redis.zset
type: qa
step: 3
---
## Q
**为什么不用红黑树**｜Redis · 跳表

有序集合要 O(log n) 的有序结构，Redis 为什么选跳表而不是平衡树？

## A
**背景。** 平衡树（比如红黑树）靠“旋转”这种局部改指针的操作保持平衡，代码细节多、不好调试。跳表换了个办法：每个节点插入时抛硬币决定长多高，靠随机而不是旋转，平均下来也是对数层。

**结构。** 同样是有序结构：平衡树靠旋转保持平衡，跳表靠随机分层。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">ZRANGE 取排名 3 到 5: 定位起点, 再顺着 L0 走</text>
<rect x="26" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="42" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">头</text>
<rect x="78" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="94" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">a</text>
<rect x="130" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="146" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">b</text>
<rect x="182" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="198" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">c</text>
<rect x="234" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="250" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">d</text>
<rect x="286" y="92" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<text x="302" y="105.85" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">e</text>
<line x1="58" y1="102" x2="78" y2="102" stroke="currentColor" stroke-width="1"/>
<polygon points="78,102 72.0,104.7 72.0,99.3" fill="currentColor"/>
<line x1="110" y1="102" x2="130" y2="102" stroke="currentColor" stroke-width="1"/>
<polygon points="130,102 124.0,104.7 124.0,99.3" fill="currentColor"/>
<line x1="162" y1="102" x2="182" y2="102" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="182,102 176.0,104.7 176.0,99.3" style="fill:var(--accent,#3b6fd4)"/>
<line x1="214" y1="102" x2="234" y2="102" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="234,102 228.0,104.7 228.0,99.3" style="fill:var(--accent,#3b6fd4)"/>
<line x1="266" y1="102" x2="286" y2="102" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="286,102 280.0,104.7 280.0,99.3" style="fill:var(--accent,#3b6fd4)"/>
<rect x="26" y="66" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="130" y="66" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="234" y="66" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<line x1="58" y1="76" x2="130" y2="76" stroke="currentColor" stroke-width="1"/>
<polygon points="130,76 124.0,78.7 124.0,73.3" fill="currentColor"/>
<line x1="162" y1="76" x2="234" y2="76" stroke="currentColor" stroke-width="1"/>
<polygon points="234,76 228.0,78.7 228.0,73.3" fill="currentColor"/>
<rect x="26" y="40" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<rect x="130" y="40" width="32" height="20" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<line x1="58" y1="50" x2="130" y2="50" style="stroke:var(--accent,#3b6fd4)" stroke-width="2"/>
<polygon points="130,50 124.0,52.7 124.0,47.3" style="fill:var(--accent,#3b6fd4)"/>
<text x="4" y="106" text-anchor="start" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L0</text>
<text x="4" y="80" text-anchor="start" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L1</text>
<text x="4" y="54" text-anchor="start" font-size="9" font-family="sans-serif" style="fill:var(--dim,#6b7280)">L2</text>
<text x="8" y="128" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">先用上层快车道定位到 b, 再下到 L0 找到 c</text>
<text x="8" y="146" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">之后 c → d → e 顺着链表走, 不用回头</text>
<text x="8" y="172" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">跳表靠随机分层保持平衡, 不用旋转, 实现和调试都简单</text>
<text x="8" y="190" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">升层概率可调, 内存能比 B 树更省</text>
<text x="8" y="208" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">范围查询把它当链表顺序遍历, 缓存局部性不比平衡树差</text>
</svg>
```

**细节。**

- 内存：调整升层概率就能调内存占用，可以比 B 树更省
- 范围查询：`ZRANGE` 把跳表当链表顺序遍历，缓存局部性至少不比平衡树差
- 简单：实现和调试都容易，加跨度字段让 `ZRANK` 变成 O(log n)，改动很小

**为什么。** 工程上简单可改，比理论最优更重要。

**对应 LeetCode：** 无直接对应的题（工程取舍）
