---
id: uth-python-gil-concurrency-1-why-gil
node: python.gil-concurrency
type: qa
step: 1
---
## Q
**为什么 CPython 要有一把 GIL**｜Python · CPython 3.14

同时开几个线程跑 Python 代码，为什么它们不能真的并行执行字节码？

## A
**背景。** 线程共享同一块内存，两个线程同时改同一个东西就会出错，最稳妥的办法是给要改的东西加锁。可 Python 里「要改的东西」太多了：每个对象都带一个引用计数（有几处在用它，降到 0 就释放），绝大多数操作都要给某些对象的计数加一或减一。给每个对象各配一把锁，开销和死锁的风险都很大。

**结构。** 默认构建里，引用计数加一就是一条普通的 `ob_refcnt = ob_refcnt + 1`，不是原子操作。下图里两个线程同时读到 5、各自写回 6：加了两次，只记了一次，计数偏小，对象会被提前释放。CPython 的办法是一把全局大锁，GIL（global interpreter lock）：同一时刻，只有持有 GIL 的线程能执行 Python 字节码。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 195">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<line x1="56" y1="76" x2="330" y2="76" stroke-dasharray="4,3"/>
<line x1="56" y1="136" x2="330" y2="136" stroke-dasharray="4,3"/>
<rect x="66" y="42" width="56" height="26" rx="3"/>
<rect x="126" y="102" width="56" height="26" rx="3"/>
<line x1="56" y1="158" x2="330" y2="158"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="190" y="42" width="56" height="26" rx="3"/>
<rect x="250" y="102" width="56" height="26" rx="3"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="330.0,158.0 324.0,161.0 324.0,155.0"/>
</g>
<g fill="currentColor">
<text x="94" y="59">读 5</text>
<text x="218" y="59">写 6</text>
<text x="154" y="119">读 5</text>
<text x="278" y="119">写 6</text>
<text x="170" y="15">ob_refcnt += 1 不是原子操作</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="30" y="60">线程 1</text>
<text x="30" y="120">线程 2</text>
<text x="330" y="174" text-anchor="end" font-size="11">时间</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="170" y="190" font-size="11">加了两次, 计数只涨 1: 对象会被提前释放</text>
</g>
</g>
</svg>
```

**细节。**

- GIL 的实现很小：一个「是否被占用」的布尔值，外加一个互斥锁和一个条件变量。
- 官方文档的说法：GIL 让对象模型（包括 `dict` 这类内置类型）隐含地对并发访问安全。

**为什么。** 单线程程序不用为加锁付任何代价，C 扩展也好写；代价是纯 Python 代码的多线程用不上多个核。

**对应 LeetCode：** 无直接对应的题
