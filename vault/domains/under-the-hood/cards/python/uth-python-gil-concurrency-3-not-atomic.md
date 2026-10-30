---
id: uth-python-gil-concurrency-3-not-atomic
node: python.gil-concurrency
type: qa
step: 3
---
## Q
**有 GIL 就线程安全吗**｜Python · CPython 3.14

4 个线程各对全局变量 `n` 做 100 万次 `n += 1`，结果一定是 4000000 吗？

## A
**背景。** GIL 保证的是「一条字节码不会被打断」，可你写的一行代码常常是好几条字节码：`n += 1` 是读 `n`、加 1、写回 `n` 三步。别的线程插在中间，就会把更新覆盖掉。

**结构。** 官方 FAQ 的清单：`L.append(x)`、`x = L[i]`、`D[x] = y` 是原子的；`i = i + 1`、`D[x] = D[x] + 1` 不是。读、改、写这类复合操作，必须自己加锁 `threading.Lock`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<line x1="102" y1="42" x2="124" y2="42"/>
<line x1="214" y1="42" x2="236" y2="42"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="12" y="28" width="90" height="28" rx="3"/>
<rect x="124" y="28" width="90" height="28" rx="3"/>
<rect x="236" y="28" width="90" height="28" rx="3"/>
<rect x="20" y="96" width="300" height="24" rx="3"/>
<rect x="20" y="132" width="78" height="24" rx="3"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="124.0,42.0 118.0,45.0 118.0,39.0"/>
<polygon points="236.0,42.0 230.0,45.0 230.0,39.0"/>
</g>
<g fill="currentColor">
<text x="170" y="16">n += 1 是三步</text>
<text x="57" y="46">LOAD n</text>
<text x="169" y="46">ADD 1</text>
<text x="281" y="46">STORE n</text>
<text x="170" y="112">3.14 (有 GIL)  4,000,000</text>
<text x="106" y="149" text-anchor="start">3.14t (无 GIL)  约 1,050,000</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="170" y="82" font-size="11">4 线程 x 100 万次, 期望 4000000 (实测)</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="170" y="185">碰巧对不是保证: 复合操作要加 Lock</text>
</g>
</g>
</svg>
```

```python
lock = threading.Lock()
with lock:
    n += 1       # 读、改、写作为一个整体，不会被别的线程插入
```

**细节。**

- 实测 3.14.8（有 GIL）：4 线程各 100 万次，两次运行结果都恰好是 4000000。原因是 CPython 只在函数入口、循环回跳、调用之后检查切换，`n += 1` 中间没有检查点，碰巧安全。
- 同一段代码用自由线程构建 3.14t 运行，实测只得到约 105 万（两次分别是 1068975 和 1051417）。

**坑。** 「碰巧对」不是语言保证，换一个解释器构建就会暴露；任何读、改、写或先检查后操作，都要自己加锁。

**对应 LeetCode：** 无直接对应的题
