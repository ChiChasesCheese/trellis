---
id: uth-python-objects-names-4-small-int
node: python.objects-names
type: qa
step: 4
---
## Q
**小整数缓存与 is 的「碰巧」**｜Python · CPython 3.14

为什么 `int("256") is int("256")` 是 `True`，`int("257") is int("257")` 却是 `False`？同一个脚本里 `x = 1000; y = 1000`，为什么又有 `x is y`？

## A
**背景。** 0、1、2 这样的小整数几乎每行代码都在用，每次用到都新建一个对象，既占内存又浪费时间。而整数不可变，谁也改不了 `5`，所以共享同一个是安全的。

**结构。** 解释器预先备好 -5 到 256 共 262 个整数对象，放在一张固定的表里；要这个范围内的整数，直接指向现成的那个，不再新建。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="20" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">预先备好 -5 到 256 共 262 个整数</text>
<rect x="20" y="30" width="44" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="42" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-5</text>
<rect x="64" y="30" width="44" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="86" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">-4</text>
<rect x="108" y="30" width="44" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="130" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">…</text>
<rect x="152" y="30" width="44" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="174" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">0</text>
<rect x="196" y="30" width="44" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="218" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="240" y="30" width="44" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="262" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">…</text>
<rect x="284" y="30" width="44" height="24" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="306" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">256</text>
<rect x="232" y="90" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="246" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">p</text>
<rect x="272" y="90" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="286" y="105" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">q</text>
<line x1="246" y1="90" x2="280" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="280.0,56.0 277.9,62.4 273.6,58.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="286" y1="90" x2="296" y2="56" stroke-width="1.2" stroke="currentColor"/>
<polygon points="296.0,56.0 297.2,62.6 291.4,60.9" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="20" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">int("256") 两次  is 真</text>
<rect x="20" y="140" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="155" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">r</text>
<rect x="20" y="176" width="28" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="34" y="191" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">s</text>
<rect x="120" y="134" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="142" y="151" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">257</text>
<rect x="120" y="172" width="44" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="142" y="189" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">257</text>
<line x1="48" y1="151" x2="118" y2="147" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,147.0 112.2,150.3 111.8,144.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="48" y1="187" x2="118" y2="185" stroke-width="1.2" stroke="currentColor"/>
<polygon points="118.0,185.0 112.1,188.2 111.9,182.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="160" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">int("257") 两次</text>
<text x="180" y="180" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">各建一个  is 假</text>
</svg>
```

**细节。**

- 范围由源码常量决定：`_PY_NSMALLNEGINTS` 是 5，`_PY_NSMALLPOSINTS` 是 257。
- 范围外的整数，运行时每次运算都新建对象，所以 `int("257") is int("257")` 为 `False`。
- 编译同一份源码时，相同的常量会合并成一个对象：脚本里 `x = 1000; y = 1000` 得到 `x is y` 为 `True`；在交互式提示符里逐行输入，每行单独编译，结果是 `False`。

**坑。** 这种「碰巧」随版本和写法变化，比较整数永远用 `==`。

**对应 LeetCode：** 无直接对应的题
