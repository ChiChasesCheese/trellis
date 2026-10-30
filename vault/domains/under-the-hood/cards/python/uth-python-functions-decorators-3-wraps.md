---
id: uth-python-functions-decorators-3-wraps
node: python.functions-decorators
type: qa
step: 3
---
## Q
**装饰后函数的名字为什么变成 wrapper**｜Python · CPython 3.14

被装饰的函数，`fib.__name__` 变成了 `'wrapper'`，文档字符串也没了。`functools.wraps` 做了什么？

## A
**背景。** 装饰之后，名字指向的是 wrapper 这个新函数，它自己的 `__name__` 就是 `'wrapper'`，也没有文档字符串。日志、调试器和按函数名登记的框架，看到的全是 `wrapper`。

**结构。** 在 wrapper 上加 `@wraps(f)`：把原函数 `f` 的元信息逐项复制过来，再设置 `__wrapped__` 指回 `f`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<rect x="10" y="28" width="122" height="92" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="71" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">fib 原函数</text>
<text x="20" y="70" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">__name__</text>
<text x="20" y="90" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">__doc__</text>
<text x="20" y="110" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">__module__</text>
<rect x="208" y="28" width="122" height="120" rx="3" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="269" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">wrapper</text>
<text x="218" y="70" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">__name__</text>
<text x="218" y="90" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">__doc__</text>
<text x="218" y="110" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">__module__</text>
<text x="218" y="136" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">__wrapped__</text>
<line x1="134" y1="66" x2="206" y2="66" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,66.0 200.0,69.0 200.0,63.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="134" y1="86" x2="206" y2="86" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,86.0 200.0,89.0 200.0,83.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="134" y1="106" x2="206" y2="106" stroke-width="1.2" stroke="currentColor"/>
<polygon points="206.0,106.0 200.0,109.0 200.0,103.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">复制</text>
<line x1="208" y1="132" x2="134" y2="112" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)" stroke-dasharray="4 3"/>
<polygon points="134.0,112.0 140.6,110.7 139.0,116.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="178" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">只复制元信息 行为不变</text>
<text x="170" y="198" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">__wrapped__ 指回原函数</text>
</svg>
```

**细节。**

- 复制的有 `__module__`、`__name__`、`__qualname__`、`__doc__` 等，并把 `f.__dict__` 合并进 wrapper 的 `__dict__`。
- `inspect.signature` 默认顺着 `__wrapped__` 找到原函数，显示原本的参数。
- `lru_cache` 内部也调用 `update_wrapper`，所以 `fib.__wrapped__` 能拿到原函数，绕过缓存。

**为什么。** 只补元信息，不改行为；代价是每个装饰器都要自己记得写这一行。

**对应 LeetCode：** 无直接对应的题
