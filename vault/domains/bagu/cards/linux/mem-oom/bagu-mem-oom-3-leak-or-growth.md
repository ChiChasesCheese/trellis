---
id: bagu-mem-oom-3-leak-or-growth
node: a.linux.mem-oom
type: qa
step: 3
---
## Q
**泄漏还是正常增长 · 怎么判断**｜必会

面试官：「内存一直在涨，怎么判断是泄漏，还是正常的增长？」

## A
**基本回答。** 看趋势和回收。泄漏是只升不降：流量降下来、触发回收之后，占用依然不回落（JVM 看 Full GC 之后老年代的占用，是否一轮比一轮高）。正常增长是随流量或缓存填充涨到一个平台就稳定，流量回落后能回落。确认之后再定位：对比不同时间点的 RSS 趋势；JVM 抓堆转储，用 MAT 看支配树（dominator tree）找占用最大的对象和引用链，比较两次转储的差异更直观。
堆转储抓两份、间隔一段时间，用 MAT 比较差异，增长最多的类型和引用链就是线索。别的语言：Go 看 heap profile，C/C++ 用 valgrind 或 jemalloc profiling。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 224">
<text x="8" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">泄漏</text>
<text x="184" y="18" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">正常增长</text>
<line x1="10" y1="30" x2="10" y2="170" stroke-width="1.2" stroke="currentColor"/>
<line x1="10" y1="170" x2="156" y2="170" stroke-width="1.2" stroke="currentColor"/>
<line x1="184" y1="30" x2="184" y2="170" stroke-width="1.2" stroke="currentColor"/>
<line x1="184" y1="170" x2="330" y2="170" stroke-width="1.2" stroke="currentColor"/>
<polyline points="14,140 34,105 38,123 42,123 62,88 66,106 70,106 90,71 94,89 98,89 118,54 122,72 126,72 146,37 150,55 154,55" stroke-width="1.5" fill="none" stroke="currentColor"/>
<polyline points="14,140 154,55" stroke-width="1.5" style="stroke:var(--accent,#3b6fd4);fill:none" stroke-dasharray="4 3"/>
<text x="14" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Full GC 之后的底线一路抬高</text>
<polyline points="188,150 205,122 225,102 250,92 275,88 292,88 306,120 326,148" stroke-width="1.5" fill="none" stroke="currentColor"/>
<text x="188" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">涨到平台，流量降就回落</text>
<text x="8" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">时间 →　纵轴是内存占用</text>
</svg>
左边是泄漏：锯齿的每次下跌是一次回收，但回收之后的底线（虚线）一轮比一轮高。右边是正常增长：涨到一个平台就稳住，流量落下来占用也跟着落下来。
**举个例子。** 打赏服务用本地 `Map` 缓存用户余额，没有上限也没有过期时间（下面的数字是演示用的假设值）：
1. **看底线：** Full GC 之后老年代的占用，周一约 600 MB，周二约 800 MB，周三约 1000 MB，每轮都更高。
2. **排除正常增长：** 周日凌晨流量最低，占用也没有回落，不像缓存涨到平台。
3. **抓两份转储：** 周一和周三各抓一份，用 MAT 比较，这个 `Map` 的 retained heap 从 200 MB 涨到 600 MB，引用链从一个静态字段出发。
4. **修复：** 改成带最大容量和过期时间的缓存，之后内存涨到一个平台就稳定了。
**容易错。**
- **内存在涨就是泄漏：** 缓存填充、流量上升都会涨。要看回收之后是否回落、有没有上限。
- **看回收之前的占用：** 里面混着垃圾，要看 Full GC 之后剩下的。
- **堆转储里没问题就没泄漏：** 直接内存、元空间这类堆外内存的泄漏不在堆转储里，要用 NMT（原生内存跟踪）查。
- **本地缓存不设上限：** 不加淘汰的 `Map` 本质上就是泄漏，只是慢一点。
