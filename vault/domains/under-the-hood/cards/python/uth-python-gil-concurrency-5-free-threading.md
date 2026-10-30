---
id: uth-python-gil-concurrency-5-free-threading
node: python.gil-concurrency
type: qa
step: 5
---
## Q
**去掉 GIL：自由线程构建怎么保证安全**｜Python · CPython 3.14

自由线程（free-threaded）的 Python 3.14 没有 GIL，引用计数还怎么保证不出错？

## A
**背景。** 想去掉 GIL，就要解决 GIL 一直替我们挡着的问题，第一个就是引用计数：全部改成原子操作会慢得多（多个核反复争抢同一份数据）。

**结构。** PEP 703 的做法：每个对象记一个「所有者线程」（`ob_tid`）。所有者增减引用走本地计数 `ob_ref_local`，是普通加减，很快；其他线程走共享计数 `ob_ref_shared`，用原子操作，慢一点。这叫偏向引用计数（biased reference counting）。内置的 `list`、`dict` 等则各带一把 1 字节的小锁（`ob_mutex`），代替 GIL 保护自己。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 230">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="10" y="54" width="100" height="26" rx="3"/>
<rect x="145" y="28" width="100" height="26" rx="3"/>
<rect x="145" y="54" width="100" height="26" rx="3"/>
<rect x="145" y="132" width="100" height="26" rx="3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="10" y="28" width="100" height="26" rx="3"/>
<rect x="145" y="80" width="100" height="26" rx="3"/>
<rect x="145" y="106" width="100" height="26" rx="3"/>
</g>
<g fill="currentColor">
<text x="60" y="45">ob_refcnt</text>
<text x="60" y="71">ob_type</text>
<text x="195" y="45" font-size="11">ob_tid</text>
<text x="195" y="71" font-size="11">ob_mutex</text>
<text x="195" y="97" font-size="11">ob_ref_local</text>
<text x="195" y="123" font-size="11">ob_ref_shared</text>
<text x="195" y="149" font-size="11">ob_type</text>
<text x="195" y="175" font-size="11">owner: 普通加减, 快</text>
<text x="195" y="193" font-size="11">其他线程: 原子操作</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="60" y="16">默认构建</text>
<text x="215" y="16">自由线程构建</text>
<text x="60" y="100" font-size="11">计数是普通整数</text>
<text x="60" y="116" font-size="11">全靠 GIL 保护</text>
<text x="252" y="45" text-anchor="start" font-size="11">owner 线程</text>
<text x="252" y="71" text-anchor="start" font-size="11">1 字节锁</text>
<text x="252" y="97" text-anchor="start" font-size="11">owner 用</text>
<text x="252" y="123" text-anchor="start" font-size="11">其他线程用</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="195" y="215" font-size="11">偏向引用计数 (PEP 703)</text>
</g>
</g>
</svg>
```

**细节。**

- 自由线程在 3.13 是实验性的，3.14 起官方支持（PEP 779），但仍是可选构建（如 `python3.14t`），默认构建依旧带 GIL。
- 数字常量、字符串字面量这类对象被设为「不朽」（immortal），引用计数永不改变。
- 单线程会变慢：官方文档给出的 pyperformance 平均开销，从 macOS aarch64 上约 1% 到 x86-64 Linux 上约 8%。
- `sys._is_gil_enabled()` 可以查当前进程里 GIL 有没有开着。

**为什么。** 用一点单线程的开销，换多核的真并行；还没适配的 C 扩展被导入时，解释器会自动把 GIL 重新打开。

**坑。** 以前被 GIL 掩盖的竞态会暴露：4 个线程各做 100 万次 `n += 1`，在自由线程构建里会丢更新。

**对应 LeetCode：** 无直接对应的题
