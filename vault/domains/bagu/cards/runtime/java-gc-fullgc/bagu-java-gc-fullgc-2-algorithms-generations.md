---
id: bagu-java-gc-fullgc-2-algorithms-generations
node: a.runtime.java-gc-fullgc
type: qa
step: 2
---
## Q
**垃圾回收 · 回收算法和分代设计**｜必会

面试官：「垃圾回收有哪几种基本算法？为什么堆要分新生代和老年代？」

## A
**基本回答。** 三种算法：标记清除（简单，留下碎片，大对象可能找不到连续空间）、标记复制（把活对象复制到另一块空区，没有碎片但浪费一半空间）、标记整理（活对象挪向一端，没有碎片也不浪费，但要移动对象并更新引用，停顿长）。分代基于「绝大多数对象朝生夕死」：新生代（Eden 加两个 Survivor）存活率低，用复制，只搬少量活对象；多次存活后晋升老年代，存活率高，复制代价太大，用清除或整理；大对象直接进老年代，免得在 Survivor 间来回复制。老年代对象指向新生代时，用卡表记下这些区域，Young GC 只额外扫它们，不必扫整个老年代。Young GC 只回收新生代，很快；Full GC 回收整个堆加元空间，停顿长，频繁出现说明有泄漏、大对象或晋升过快。并发标记用三色标记加屏障防漏标，G1 用原始快照（SATB）。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">堆（heap）分成新生代和老年代</text>
<text x="113" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">新生代</text>
<text x="280" y="34" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">老年代</text>
<rect x="8" y="42" width="110" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63.0" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Eden</text>
<text x="63.0" y="73.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新对象先住这</text>
<rect x="118" y="42" width="50" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="143.0" y="66.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">S0</text>
<rect x="168" y="42" width="50" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="193.0" y="66.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">S1</text>
<rect x="228" y="42" width="104" height="40" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="280.0" y="58.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">老年代</text>
<text x="280.0" y="73.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长期存活</text>
<line x1="218" y1="62" x2="228" y2="62" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="228.0,62.0 221.0,65.2 221.0,58.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="8" y="106" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">① 新对象先放 Eden</text>
<text x="8" y="124" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">② Young GC：活的复制到空的 Survivor</text>
<text x="8" y="142" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">③ 活过多次 → 晋升老年代</text>
<text x="8" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">④ 老年代指向新生代：卡表记下区域</text>
<text x="8" y="184" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Young GC 只扫新生代，不扫整个老年代</text>
</svg>
新对象进 Eden，Young GC 把活的复制到空的 Survivor，活过多次的晋升老年代；老年代里指向新生代的引用，用卡表记下来。
**业务场景。** 聊天网关每条消息产生大量临时对象，死在新生代，Young GC 很快；若把离线消息攒在内存队列里，它们长期存活、晋升老年代，老年代涨满触发 Full GC，应当落到存储而不是留在堆里。
**容易错。**
- **以为 Young GC 要扫整个堆：** 借助卡表，只扫新生代加有跨代引用的老年代区域。
