---
id: bagu-java-gc-fullgc-6-tune-verify
node: a.runtime.java-gc-fullgc
type: qa
step: 6
---
## Q
**Full GC 排查 · 排查完怎么调优和验证**｜追问

面试官：「你定位到原因、也改了，怎么证明问题真的解决了？调参数有什么原则？」

## A
**基本回答。** 先定目标（如 P99 停顿小于某个值，没有目标就没法判断）；每次只改一个变量（堆大小、新生代比例、收集器或停顿目标），同时改多个就分不清好坏；用接近线上流量的压测对比 GC 日志里的停顿和频率，先灰度一台再放量。能不调参就不调，优先修泄漏和大对象；只加大堆是推后故障，还可能让单次停顿和堆转储更大。验证看趋势：GC 停顿 P99、GC 占 CPU 比例、回收后老年代占用、对象分配速率，并把这些放进监控和发布检查。容器里堆要小于内存限制，留出元空间、线程栈、直接内存，否则被 OOMKilled。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 262">
<rect x="8" y="8" width="170" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="26.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">① 定目标：P99 停顿</text>
<rect x="8" y="48" width="170" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="66.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">② 每次只改一个变量</text>
<line x1="93" y1="44" x2="93" y2="48" stroke-width="1.2" stroke="currentColor"/>
<polygon points="93.0,48.0 89.8,41.0 96.2,41.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="88" width="170" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="93.0" y="106.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">③ 压测对比 GC 日志</text>
<line x1="93" y1="84" x2="93" y2="88" stroke-width="1.2" stroke="currentColor"/>
<polygon points="93.0,88.0 89.8,81.0 96.2,81.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="128" width="170" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="146.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">④ 先灰度一台</text>
<line x1="93" y1="124" x2="93" y2="128" stroke-width="1.2" stroke="currentColor"/>
<polygon points="93.0,128.0 89.8,121.0 96.2,121.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="168" width="170" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="93.0" y="186.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">⑤ 再放量</text>
<line x1="93" y1="164" x2="93" y2="168" stroke-width="1.2" stroke="currentColor"/>
<polygon points="93.0,168.0 89.8,161.0 96.2,161.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="196" y="62" width="136" height="92" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="264.0" y="82.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">看趋势指标</text>
<text x="264.0" y="97.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GC 停顿 P99</text>
<text x="264.0" y="112.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GC 占 CPU 比例</text>
<text x="264.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">回收后老年代占用</text>
<text x="264.0" y="142.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">对象分配速率</text>
<line x1="178" y1="102" x2="196" y2="102" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="196.0,102.0 189.0,105.2 189.0,98.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="226" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">容器里：堆 + 元空间 + 线程栈 + 直接内存</text>
<text x="8" y="246" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">合起来要小于容器内存限制，否则 OOMKilled</text>
</svg>
左边是调优的五步，按顺序走；第三步压测之后，用右边四个趋势指标判断好没好。最下面提醒：容器里各块内存加起来不能超过限额。
**业务场景。** 开票前一周压测，GC 日志显示 Full GC 平均每分钟一次，回收后老年代不降，堆转储发现缓存没有上限；只给缓存加上限、其他参数不动，重跑同样压测，Full GC 降为零，才进入开票演练。
**容易错。**
- **压测流量和线上差很远：** 结论不可信。
