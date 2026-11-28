---
id: bagu-java-jvm-memory-classload-1-regions-classloader
node: b.runtime.java-jvm-memory-classload
type: qa
step: 1
---
## Q
**JVM 内存区域与类加载 · 双亲委派怎么打破**｜追问

面试官：「线上报 Metaspace OOM 和 ClassNotFoundException，你从哪几块内存、哪条类加载链去查？」

## A
**基本回答。** 线程共享的有堆（对象，分新生代、老年代；默认最大堆是物理内存的 1/4）和方法区（HotSpot 里是元空间 Metaspace，在本地内存，`MaxMetaspaceSize` 默认无上限）；线程私有的有虚拟机栈、本地方法栈、程序计数器。类加载三步：加载、链接（验证、准备、解析）、初始化。双亲委派：先交给父加载器，父加载不了才自己加载，链是应用 → 平台 → 启动类加载器（JDK 9 起平台取代扩展）；好处是核心类不被篡改、同一个类只加载一份。`String` 的加载器是 null（启动类加载器），`java.sql.Connection` 是平台类加载器。打破它的有：SPI 用线程上下文类加载器（接口在上层、实现在下层，如 JDBC 驱动），Tomcat 每个 Web 应用独立加载器，OSGi 和热部署。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 232">
<rect x="6" y="10" width="178" height="212" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="95" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="95" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">线程共享</text>
<rect x="14" y="38" width="162" height="86" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="95" y="56" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">堆：放对象</text>
<rect x="22" y="64" width="68" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="56" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新生代</text>
<rect x="96" y="64" width="72" height="50" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="132" y="93" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">老年代</text>
<rect x="14" y="134" width="162" height="78" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="95" y="154.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">方法区</text>
<text x="95" y="169.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">HotSpot 里是元空间</text>
<text x="95" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Metaspace，本地内存</text>
<text x="95" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">默认无上限</text>
<rect x="196" y="10" width="138" height="212" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="265" y="120" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor"></text>
<text x="265" y="28" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">线程私有</text>
<rect x="204" y="40" width="122" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="62.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">虚拟机栈</text>
<text x="265" y="77.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">方法调用的栈帧</text>
<rect x="204" y="102" width="122" height="52" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="124.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">本地方法栈</text>
<text x="265" y="139.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">native 方法</text>
<rect x="204" y="164" width="122" height="48" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="265" y="184.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">程序计数器</text>
<text x="265" y="199.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">当前执行到哪行</text>
</svg>
左边虚线框是线程共享的堆和元空间；右边是每个线程私有的三块。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 296">
<text x="8" y="16" text-anchor="acc" font-size="12" font-family="sans-serif" fill="currentColor">类加载器链：先问父亲，父亲不行才自己来</text>
<rect x="8" y="28" width="140" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="49" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">应用类加载器</text>
<rect x="8" y="84" width="140" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="78" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">平台类加载器</text>
<rect x="8" y="140" width="140" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="78" y="161" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">启动类加载器</text>
<line x1="60" y1="62" x2="60" y2="77" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60.0,84.0 56.8,77.0 63.2,77.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="60" y1="118" x2="60" y2="133" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="60.0,140.0 56.8,133.0 63.2,133.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="66" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">委派</text>
<text x="66" y="132" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">委派</text>
<text x="160" y="44" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">你自己的类</text>
<text x="160" y="100" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">java.sql.Connection</text>
<text x="160" y="150" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">String、ArrayList</text>
<text x="160" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">getClassLoader() 为 null</text>
<text x="8" y="204" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">类加载三步：</text>
<rect x="8" y="214" width="70" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="43" y="235" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">加载</text>
<rect x="94" y="214" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="169" y="227.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">链接</text>
<text x="169" y="242.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">验证 准备 解析</text>
<rect x="260" y="214" width="72" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="296" y="235" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">初始化</text>
<line x1="78" y1="231" x2="87" y2="231" stroke-width="1.2" stroke="currentColor"/>
<polygon points="94.0,231.0 87.0,234.2 87.0,227.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="244" y1="231" x2="253" y2="231" stroke-width="1.2" stroke="currentColor"/>
<polygon points="260.0,231.0 253.0,234.2 253.0,227.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="8" y="280" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">核心类不被篡改，同一个类只加载一份</text>
</svg>
上半是三个类加载器的委派关系，右边写了每个类由谁加载；下半是类加载的三个阶段。
**举个例子。** 反复热部署后报 Metaspace OOM：每次部署 Tomcat 新建一个类加载器加载全部类。旧加载器没有引用才会被回收；若静态变量或线程池里的线程还引用着它里面的对象，它加载的所有类都留在元空间，部署 10 次就有 10 份重复的类，直到本地内存耗尽。处理是找到并释放引用，并设 `-XX:MaxMetaspaceSize` 兜底，让问题早暴露而不是拖垮整台机器。ClassNotFoundException 则是应用 A 的加载器沿委派链往上都看不见类，类实际在应用 B 的加载器里。
**容易错。**
- **把 Metaspace OOM 当成堆不够：** 要看是不是动态生成类（CGLIB、反射、Groovy）太多或类加载器泄漏。
- **以为元空间在堆里：** 在本地内存，默认不设上限，要自己限制。
- **把 getClassLoader() 为 null 当成出错：** 那是启动类加载器加载的核心类。
