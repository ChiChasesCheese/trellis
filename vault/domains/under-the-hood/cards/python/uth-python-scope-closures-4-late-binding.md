---
id: uth-python-scope-closures-4-late-binding
node: python.scope-closures
type: qa
step: 4
---
## Q
**循环里的 lambda 为什么都拿到最后一个值**｜Python · CPython 3.14

`fs = [lambda: i for i in range(3)]` 之后，`[f() for f in fs]` 为什么是 `[2, 2, 2]`？怎样得到 `[0, 1, 2]`？

## A
**背景。** 你想让每个 lambda 记住「创建它时的 `i`」。可闭包记住的是 cell（变量本身），不是值的快照。

**结构。** 整个循环只有一个变量 `i`，所有 lambda 共用同一个 cell。lambda 被调用时才去读 cell，那时循环早已结束，cell 里是最后一个值 2。这叫晚绑定（late binding）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 235">
<text x="10" y="16" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">lambda: i</text>
<rect x="10" y="26" width="60" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="41" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f0</text>
<line x1="70" y1="37" x2="198" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="198.0,64.0 191.5,65.7 192.7,59.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="54" width="60" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="69" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f1</text>
<line x1="70" y1="65" x2="198" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="198.0,64.0 192.0,67.0 192.0,61.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="82" width="60" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="97" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f2</text>
<line x1="70" y1="93" x2="198" y2="64" stroke-width="1.2" stroke="currentColor"/>
<polygon points="198.0,64.0 192.8,68.3 191.5,62.4" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="200" y="44" width="110" height="40" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="255" y="68" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">cell  i = 2</text>
<text x="255" y="104" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">调用时才读 cell</text>
<line x1="10" y1="124" x2="330" y2="124" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="144" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">lambda i=i: i</text>
<rect x="10" y="154" width="60" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f0</text>
<rect x="100" y="154" width="130" height="22" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="165" y="169" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">默认值 0</text>
<line x1="70" y1="165" x2="98" y2="165" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,165.0 92.0,168.0 92.0,162.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="182" width="60" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="197" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f1</text>
<rect x="100" y="182" width="130" height="22" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="165" y="197" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">默认值 1</text>
<line x1="70" y1="193" x2="98" y2="193" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,193.0 92.0,196.0 92.0,190.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="10" y="210" width="60" height="22" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="40" y="225" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">f2</text>
<rect x="100" y="210" width="130" height="22" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="165" y="225" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">默认值 2</text>
<line x1="70" y1="221" x2="98" y2="221" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,221.0 92.0,224.0 92.0,218.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="240" y="190" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">定义时就存好</text>
</svg>
```

**细节。**

- 修法一：`lambda i=i: i`。默认值在 lambda 创建那一刻求值，存进 `__defaults__`，每个 lambda 一份。
- 修法二：`functools.partial`，或再套一层工厂函数，让每次调用产生新的 cell。
- 这不是 lambda 独有的，普通 `def` 的闭包同理。

**为什么。** 共享 cell，外层之后的修改才能被内层看到；代价就是这个陷阱。

**对应 LeetCode：** 无直接对应的题
