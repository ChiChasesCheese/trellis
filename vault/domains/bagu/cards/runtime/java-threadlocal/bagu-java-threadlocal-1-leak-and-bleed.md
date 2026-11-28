---
id: bagu-java-threadlocal-1-leak-and-bleed
node: b.runtime.java-threadlocal
type: qa
step: 1
---
## Q
**ThreadLocal · 原理、内存泄漏和线程池串号**｜追问

面试官：「ThreadLocal 为什么会内存泄漏？在线程池里用它还有什么坑？」

## A
**基本回答。** 值存在当前线程的 `ThreadLocalMap` 里，ThreadLocal 对象只是 key，所以各线程互不干扰。key 是弱引用、value 是强引用：ThreadLocal 失去外部引用被 GC 后 key 变 null，value 仍被 map 强引用，map 又被存活的线程引用，线程池里不退出的线程让这些 value 永远回收不掉，就是泄漏。更常见更危险的是串号：线程被复用，上个请求没清的用户信息被下个请求读到。做法：用完在 `finally` 里 `remove()`，声明为 `static final`。`InheritableThreadLocal` 只在创建线程时复制一次，对早已建好的线程池线程无效，要用 `TransmittableThreadLocal` 或显式传参。
**2026 亮点。** `ScopedValue` 生命周期限定在作用域内、结束自动失效，适合虚拟线程；JDK 21 预览，JDK 25 定稿。
**先看图。**
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 270">
<rect x="8" y="12" width="150" height="34" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="25.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">线程池里的 Thread</text>
<text x="83" y="40.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">（长寿，一直不退出）</text>
<line x1="83" y1="46" x2="83" y2="57" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,64.0 79.8,57.0 86.2,57.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="64" width="150" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="83" y="83" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ThreadLocalMap</text>
<line x1="83" y1="94" x2="83" y2="105" stroke-width="1.2" stroke="currentColor"/>
<polygon points="83.0,112.0 79.8,105.0 86.2,105.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="8" y="112" width="150" height="62" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">Entry</text>
<text x="83" y="147" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">key：弱引用</text>
<text x="83" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">value：强引用</text>
<rect x="196" y="112" width="138" height="62" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="265" y="132" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ThreadLocal 对象</text>
<text x="265" y="147" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">外部没引用了</text>
<text x="265" y="162" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">GC 回收，key 变 null</text>
<line x1="158" y1="130" x2="189" y2="130" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="196.0,130.0 189.0,133.2 189.0,126.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="166" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">弱</text>
<line x1="83" y1="174" x2="83" y2="189" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="83.0,196.0 79.8,189.0 86.2,189.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="8" y="196" width="150" height="34" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="83" y="209.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">value：用户信息</text>
<text x="83" y="224.5" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">还在，回收不掉</text>
<text x="172" y="214" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">← 强引用一路连到线程</text>
<text x="8" y="254" text-anchor="dim" font-size="12" font-family="sans-serif" fill="currentColor">不 remove：泄漏 + 下个请求读到上个用户</text>
</svg>
左边一条线：Thread 引用 map，map 引用 Entry，Entry 对 value 是强引用。右边的 ThreadLocal 对象被回收后 key 变 null，value 还被这条强引用链挂着。
**举个例子。** 线程池只有 worker-1，存当前用户：任务 1 处理 alice 并 `set("alice")` 没 `remove`；任务 2 是 bob 的请求，若在 `set` 前先 `get`，读到 alice，bob 的操作记到 alice 名下。实测不 `remove` 读到 alice，`remove` 后读到 null。正确写法 `try { set(user); 处理 } finally { remove(); }`。
**容易错。**
- **以为弱引用 key 就不泄漏：** key 被回收后 value 的强引用还在，value 是大对象时内存一直占着。
- **把 ThreadLocal 当全局变量：** 它是线程内的隐式参数，生命周期要自己管。
