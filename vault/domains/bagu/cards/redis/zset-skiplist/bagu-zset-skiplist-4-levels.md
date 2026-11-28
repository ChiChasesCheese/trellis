---
id: bagu-zset-skiplist-4-levels
node: a.redis.zset-skiplist
type: qa
step: 4
---
## Q
**跳表 · 层数怎么定，查找插入为什么是 O(log N)**｜追问

面试官：「跳表的层数怎么决定？为什么查找和插入是 O(log N)？最坏情况呢？」

## A
**基本回答。** 新节点先有 1 层，然后每次以 25% 的概率再升一层，直到没抽中或到上限 32 层（6.0 起；5.0 是 64）。第 k 层约剩 (1/4)^(k-1) 的节点，总层数期望约 log4 N。查找从最高层往右走，下一个节点分数太大就下沉一层，每层期望走常数步，合起来期望 O(log N)。插入：照查找路径记下每层的前驱，随机出层数，逐层接入并修正跨度，只改局部指针，没有旋转。p 取 1/4 而非 1/2：层数和指针更少，更省内存，代价是每层多走几步。名次靠沿路径累加跨度；`ZRANGE 0 99` 先用跨度 O(log N) 定位第 0 个，再走 99 步。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 222">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">找 21：蓝色路径，从最高层开始</text>
<text x="8" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">最底层 L1 是完整有序链表</text>
<rect x="8" y="30" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="27.0" y="46.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">头</text>
<rect x="8" y="74" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="27.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">头</text>
<rect x="8" y="118" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="27.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">头</text>
<rect x="58" y="118" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="77.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="102" y="118" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="121.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="102" y="74" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="121.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="146" y="118" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="165.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">12</text>
<rect x="190" y="118" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="209.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">17</text>
<rect x="190" y="74" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="209.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">17</text>
<rect x="190" y="30" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="209.0" y="46.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">17</text>
<rect x="234" y="118" width="38" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="253.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">21</text>
<rect x="278" y="118" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297.0" y="134.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">26</text>
<rect x="278" y="74" width="38" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="297.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">26</text>
<line x1="46" y1="42" x2="190" y2="42" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190.0,42.0 183.0,45.2 183.0,38.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="46" y1="86" x2="102" y2="86" stroke-width="1.2" stroke="currentColor"/>
<polygon points="102.0,86.0 95.0,89.2 95.0,82.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="140" y1="86" x2="190" y2="86" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,86.0 183.0,89.2 183.0,82.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="228" y1="86" x2="278" y2="86" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="278.0,86.0 271.0,89.2 271.0,82.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="46" y1="130" x2="58" y2="130" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58.0,130.0 51.0,133.2 51.0,126.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="96" y1="130" x2="102" y2="130" stroke-width="1.2" stroke="currentColor"/>
<polygon points="102.0,130.0 95.0,133.2 95.0,126.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="140" y1="130" x2="146" y2="130" stroke-width="1.2" stroke="currentColor"/>
<polygon points="146.0,130.0 139.0,133.2 139.0,126.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="184" y1="130" x2="190" y2="130" stroke-width="1.2" stroke="currentColor"/>
<polygon points="190.0,130.0 183.0,133.2 183.0,126.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="228" y1="130" x2="234" y2="130" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="234.0,130.0 227.0,133.2 227.0,126.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="272" y1="130" x2="278" y2="130" stroke-width="1.2" stroke="currentColor"/>
<polygon points="278.0,130.0 271.0,133.2 271.0,126.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="209" y1="54" x2="209" y2="74" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="209.0,74.0 205.8,67.0 212.2,67.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="209" y1="98" x2="209" y2="118" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="209.0,118.0 205.8,111.0 212.2,111.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="205" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">L3 → 17；L2 下一个 26 太大，下沉；L1 → 21</text>
<text x="8" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">虚线箭头：26 > 21，不走，下沉一层</text>
</svg>
找 21：先在最高层（L3）从头直接跳到 17，L2 的下一个是 26，太大了，不走，下沉到 L1，再往右一步就是 21。蓝色箭头就是走过的路。
**业务场景。** 百万主播的榜单：第 1 层约 100 万个节点，第 2 层约 25 万，第 3 层约 6.3 万，到第 10 层只剩约 4 个，所以最高约 10 层，一次 `ZREVRANK` 比较几十次，榜单变长也不明显变慢（模拟平均每节点 1.334 个指针，与理论值 1/(1-p) 一致）。真正的限制是单线程总吞吐。
**容易错。**
- **以为最坏也是 O(log N)：** O(log N) 是期望；运气极差退化成 O(N)，概率可忽略。
- **以为层数有规则：** 完全随机，插入顺序不同，跳表长得不同。
