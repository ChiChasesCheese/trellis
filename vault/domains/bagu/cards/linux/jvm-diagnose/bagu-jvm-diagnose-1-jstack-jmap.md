---
id: bagu-jvm-diagnose-1-jstack-jmap
node: b.linux.jvm-diagnose
type: qa
step: 1
---
## Q
**JVM 线上诊断 · jstack、jmap、jstat 与 MAT**｜追问

面试官：「线上 Java 服务 Full GC 频繁，你用什么工具排查？怎么用 jstack 定位死锁和 CPU 高？」

## A
**基本回答。** `jstat` 看 GC 趋势，`jstack` 看线程栈，`jmap` 导出堆转储，再用 MAT 分析大对象和引用链，最后决定是调参数还是改代码。
死锁：`jstack` 末尾直接输出 `Found one Java-level deadlock`。CPU 高：`top -H -p` 找线程，转十六进制找 `nid=0x…`。MAT 重点看 Dominator Tree 和到 GC Roots 的引用链。`jmap -dump:live` 还会触发 Full GC。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 316">
<rect x="110" y="6" width="120" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="170" y="23" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Java 服务异常</text>
<line x1="140" y1="32" x2="91.7" y2="46.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,48 90.8,43.0 92.6,49.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="200" y1="32" x2="248.3" y2="46.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,48 247.4,49.1 249.2,43.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="48" width="158" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="85" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Full GC 频繁</text>
<rect x="176" y="48" width="158" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="66" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程卡住 / CPU 高</text>
<line x1="85" y1="76" x2="85.0" y2="83.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,90 81.8,83.0 88.2,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="255" y1="76" x2="255.0" y2="83.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,90 251.8,83.0 258.2,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="90" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">jstat -gcutil</text>
<text x="85" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">看 FGC、老年代趋势</text>
<rect x="176" y="90" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="108.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">jstack &lt;pid&gt;</text>
<text x="255" y="123.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">间隔几秒多抓几次</text>
<line x1="85" y1="134" x2="85.0" y2="141.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,148 81.8,141.0 88.2,141.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="255" y1="134" x2="255.0" y2="141.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,148 251.8,141.0 258.2,141.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="148" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="166.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">jmap -dump:live</text>
<text x="85" y="181.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">导出堆（会 Full GC）</text>
<rect x="176" y="148" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="166.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">末尾有 Found one</text>
<text x="255" y="181.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Java-level deadlock</text>
<line x1="85" y1="192" x2="85.0" y2="199.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="85,206 81.8,199.0 88.2,199.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="255" y1="192" x2="255.0" y2="199.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="255,206 251.8,199.0 258.2,199.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="6" y="206" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="85" y="224.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">MAT 分析堆</text>
<text x="85" y="239.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Dominator Tree</text>
<rect x="176" y="206" width="158" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="224.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CPU 高：top -H 找</text>
<text x="255" y="239.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">TID，转 nid=0x…</text>
<rect x="6" y="266" width="328" height="44" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="170" y="284.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">OOM 时自动留证据：</text>
<text x="170" y="299.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-XX:+HeapDumpOnOutOfMemoryError</text>
</svg>
左边是内存问题：先看趋势，再导出堆，最后分析是谁占着内存。右边是线程问题：抓栈看死锁，或把最忙的线程对应到栈。最下面的参数让 OOM 时自动留现场。
**举个例子。** 批量结算服务 Full GC 频繁：
1. **看趋势：** `jstat -gcutil <pid> 1000 5` 连续采样，老年代使用率一直往上涨、FGC 次数不断增加，Full GC 之后也降不下来。
2. **摘流量：** 取堆转储会停顿应用，先把这台机器从流量里摘掉。
3. **导出堆：** `jmap -dump:live,format=b,file=heap.hprof <pid>`。
4. **MAT 分析：** 在 Dominator Tree 里发现一个缓存 Map 占了大半堆，引用链从 GC Roots 一路指向它，说明它一直不被释放。
5. **改代码：** 改为带容量上限的缓存，Full GC 频率恢复正常。
6. **死锁的例子：** `jstack <pid>` 末尾输出 `Found one Java-level deadlock`：线程 A 持有锁 1、等锁 2，线程 B 持有锁 2、等锁 1，互相等待。
**容易错。**
- **只抓一次 jstack：** 瞬间的栈可能不在热点，多抓几次，同一线程栈不变才说明卡住。
- **线上直接 jmap：** 会停顿应用、还会触发 Full GC，大堆要先摘流量，并准备足够磁盘。
- **一遇到 Full GC 就加大堆：** 有泄漏时加堆只是推迟，应先看 MAT 里是谁占着内存。
- **没配 OOM 自动转储：** 出事时现场就没了，要提前配 `-XX:+HeapDumpOnOutOfMemoryError`。
- **十进制线程号直接搜 jstack：** 要先转十六进制再找 `nid=0x…`。
