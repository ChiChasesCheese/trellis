---
id: bagu-java-language-basics-1-string-equals-io
node: b.runtime.java-language-basics
type: qa
step: 1
---
## Q
**Java 基础 · String 不可变、equals/hashCode、IO 模型**｜追问

面试官：「String 为什么不可变？为什么重写 equals 必须重写 hashCode？BIO、NIO、AIO 有何区别？」

## A
**基本回答。** String 是 final 类，内部数组私有、没有修改方法，所以线程安全、hash 值可缓存、适合做 HashMap 的 key，常量池才能复用同一个对象（字面量 `"ab"` 进池，`new String("ab")` 在堆上新建，`intern()` 取池中对象）；代价是拼接产生新对象，循环里用 StringBuilder。HashMap 先按 hashCode 找桶、再用 equals 核对，所以相等的对象必须有相同 hashCode；只重写 equals，`get` 返回 null，HashSet 里还出现重复元素，`record` 自动生成两者就正常。BIO 每个连接一个线程、读写阻塞；NIO 用 Selector 多路复用，一个线程管多个连接（Linux 底层 epoll），Netty 基于它；AIO 是完成后回调，实际很少用。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只重写 equals、没重写 hashCode（8 个桶，示意）</text>
<rect x="66" y="28" width="100" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="116.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k2 → 桶 2</text>
<rect x="180" y="28" width="150" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="255.0" y="45.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k1 → 桶 5</text>
<rect x="26" y="100" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="44" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="62" y="100" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="80" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="98" y="100" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="116" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="134" y="100" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="152" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="170" y="100" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="188" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="206" y="100" width="36" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="224" y="118" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k1</text>
<text x="224" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">5</text>
<rect x="242" y="100" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="260" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">6</text>
<rect x="278" y="100" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="296" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">7</text>
<line x1="255" y1="54" x2="224" y2="100" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="224.0,100.0 225.2,93.1 229.9,96.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<line x1="116" y1="54" x2="116" y2="100" stroke-width="1.2" stroke="currentColor"/>
<polygon points="116.0,100.0 113.1,93.6 118.9,93.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="10" y="168" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">get(k2) 去桶 2 找，空的 → 返回 null</text>
<text x="10" y="186" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">k1.equals(k2) 是 true，但 hashCode 不同</text>
</svg>
k1 放进桶 5；内容相同的 k2 因为 hashCode 不同，算出桶 2，那里是空的，所以 get 返回 null。
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 212">
<text x="10" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">BIO：一连接一线程</text>
<text x="185" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">NIO：一线程管多个</text>
<rect x="10" y="30" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="32.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接1</text>
<line x1="54" y1="43" x2="90" y2="43" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,43.0 83.6,45.9 83.6,40.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="90" y="30" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 1</text>
<rect x="185" y="30" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="207.0" y="47.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接1</text>
<line x1="229" y1="43" x2="247" y2="43" stroke-width="1.2" stroke="currentColor"/>
<polygon points="247.0,43.0 240.6,45.9 240.6,40.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="70" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="32.0" y="87.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接2</text>
<line x1="54" y1="83" x2="90" y2="83" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,83.0 83.6,85.9 83.6,80.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="90" y="70" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="87.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 2</text>
<rect x="185" y="70" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="207.0" y="87.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接2</text>
<line x1="229" y1="83" x2="247" y2="83" stroke-width="1.2" stroke="currentColor"/>
<polygon points="247.0,83.0 240.6,85.9 240.6,80.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="110" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="32.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接3</text>
<line x1="54" y1="123" x2="90" y2="123" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,123.0 83.6,125.9 83.6,120.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="90" y="110" width="60" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="120.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程 3</text>
<rect x="185" y="110" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="207.0" y="127.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">连接3</text>
<line x1="229" y1="123" x2="247" y2="123" stroke-width="1.2" stroke="currentColor"/>
<polygon points="247.0,123.0 240.6,125.9 240.6,120.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="247" y="30" width="70" height="106" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="282.0" y="79.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Selector</text>
<text x="282.0" y="94.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（epoll）</text>
<line x1="282" y1="136" x2="282" y2="160" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="282.0,160.0 279.1,153.6 284.9,153.6" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="247" y="160" width="70" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="282.0" y="177.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1 个线程</text>
<text x="10" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">线程多，阻塞时各自空等</text>
<text x="185" y="206" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">谁就绪就处理谁</text>
</svg>
BIO 每个连接占一个线程，阻塞时只能空等；NIO 让一个线程通过 Selector 管多个连接，谁就绪处理谁。
**举个例子。** 订单号对象 `OrderKey("A1")` 只重写了 equals：`put(k1, 订单)` 时 k1 的 hashCode 是默认的对象地址派生值，落在桶 5；另 new 的 k2 `equals` 为 true，但算出桶 2，是空的，`get(k2)` 返回 null，缓存永远命不中，每次都回源数据库。同时重写 hashCode 后 k2 也落桶 5，再用 equals 核对成功。
**容易错。**
- **用 `==` 比包装类型：** `Integer` 只缓存 -128 到 127，128 以上 `==` 为 false，要用 equals。
- **以为 String 不可变是为了省内存：** 主要是线程安全、hash 可缓存、常量池复用。
- **finally 里 return：** 会覆盖 try 里的返回值（实测返回 2）。
