---
id: bagu-java-gc-fullgc-1-reachability
node: a.runtime.java-gc-fullgc
type: qa
step: 1
---
## Q
**垃圾回收 · JVM 怎么判断对象已死，GC Roots 有哪些**｜必会

面试官：「JVM 怎么知道一个对象可以回收了？为什么不用引用计数？哪些对象算 GC Roots？」

## A
**基本回答。** 用可达性分析：从 GC Roots 沿引用遍历，走不到的对象就是垃圾。GC Roots 包括线程栈里的局部变量、类的静态变量、常量引用、本地方法（JNI）持有的引用。不用引用计数：两个对象互相引用时计数都是 1，外面已没人指向却永远不为 0（循环引用）；每次赋值还要改计数，多线程下要同步，开销大。回收器只问「走不走得到」，不问业务上还用不用，所以忘了断开的引用就是内存泄漏；标记期间应用线程仍在改引用，会漏标错标，所以要停顿或写屏障。四种引用：强引用不回收；软引用内存不足才回收，适合缓存；弱引用下次 GC 回收（`WeakHashMap`）；虚引用用于回收通知。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 218">
<text x="8" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">从 GC Roots 出发，走得到的才算活</text>
<rect x="8" y="30" width="80" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="48.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">局部变量</text>
<rect x="8" y="72" width="80" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="48.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">静态变量</text>
<rect x="130" y="30" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="155.0" y="48.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">A</text>
<rect x="130" y="72" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="155.0" y="90.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">B</text>
<rect x="226" y="51" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="251.0" y="69.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">C</text>
<line x1="88" y1="44" x2="130" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="130.0,44.0 123.0,47.2 123.0,40.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="88" y1="86" x2="130" y2="86" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="130.0,86.0 123.0,89.2 123.0,82.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="180" y1="44" x2="226" y2="59" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="226.0,59.0 218.4,59.9 220.3,53.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="180" y1="86" x2="226" y2="71" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="226.0,71.0 220.3,76.2 218.4,70.1" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="284" y="69" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">保留</text>
<rect x="8" y="116" width="324" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<rect x="60" y="126" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85.0" y="144.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">D</text>
<rect x="230" y="126" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255.0" y="144.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">E</text>
<line x1="110" y1="134" x2="230" y2="134" stroke-width="1.2" stroke="currentColor"/>
<polygon points="230.0,134.0 223.0,137.2 223.0,130.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="230" y1="146" x2="110" y2="146" stroke-width="1.2" stroke="currentColor"/>
<polygon points="110.0,146.0 117.0,142.8 117.0,149.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="171" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有任何 Root 指向它们</text>
<text x="8" y="196" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">D、E 互相指着，引用计数各为 1，回收不掉</text>
<text x="8" y="212" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">可达性分析走不到它们 → 垃圾</text>
</svg>
左边是 GC Roots，沿箭头走得到的 A、B、C 全部保留；下面的 D、E 互相引用，但没有任何 Root 指向它们，走不到，所以是垃圾。
**业务场景。** 进程内缓存用无上限的静态 HashMap 存商品详情，运行几天后老年代一直涨、每次回收释放不了多少：Root → 静态变量 → Map → 商品详情这条路一直通，回收器认为都活着，最终 OOM；加容量上限和过期后恢复正常。常见泄漏路径还有没清理的 ThreadLocal、没注销的监听器、没关闭的连接或流。
**容易错。**
- **混淆软引用和弱引用：** 软引用内存不足才回收，弱引用下一次 GC 就回收。
