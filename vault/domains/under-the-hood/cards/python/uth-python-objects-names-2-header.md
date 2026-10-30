---
id: uth-python-objects-names-2-header
node: python.objects-names
type: qa
step: 2
---
## Q
**每个对象的头里有什么**｜Python · CPython 3.14

整数 `1` 在 Python 里占 28 字节（`sys.getsizeof(1)`），C 的 `int` 只要 4 字节。多出来的是什么？每个对象都带着哪两样东西？

## A
**背景。** 名字能指向任何类型的对象。解释器顺着指针拿到一个对象，必须马上知道两件事：它是什么类型？还有没有名字在用它？这两个答案存不进名字里，只能由对象自己带着。

**结构。** 每个对象开头都有一个固定的头：引用计数（reference count，有多少个名字或容器指着它）和类型指针（指向它的类型对象）。64 位、有 GIL 的普通构建里，头共 16 字节。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<text x="6" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">整数 1 在内存里</text>
<rect x="6" y="52" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="21" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">x</text>
<line x1="36" y1="66" x2="58" y2="66" stroke-width="1.2" stroke="currentColor"/>
<polygon points="58.0,66.0 52.0,69.0 52.0,63.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="60" y="52" width="60" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="90" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">引用计数</text>
<rect x="120" y="52" width="60" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="150" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">类型指针</text>
<rect x="180" y="52" width="60" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="210" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">长度符号</text>
<rect x="240" y="52" width="30" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="255" y="70" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">值 1</text>
<line x1="60" y1="44" x2="180" y2="44" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="120" y="36" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">对象头 16 字节</text>
<line x1="180" y1="88" x2="270" y2="88" stroke-width="1.2" stroke="currentColor"/>
<text x="225" y="106" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">整数自己 12 字节</text>
<text x="190" y="130" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">合计 28 字节</text>
<rect x="70" y="146" width="100" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="120" y="164" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">int 类型对象</text>
<line x1="150" y1="80" x2="120" y2="146" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="120.0,146.0 119.8,139.3 125.2,141.8" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="190" y="164" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">类型指针指向它</text>
</svg>
```

**细节。**

- 整数 `1` = 头 16 字节 + 长度与符号 8 字节 + 数值 4 字节 = 28 字节；`sys.getsizeof(object())` 是 16，只有头。
- `type(x)` 就是读类型指针；查找 `x.append` 也从它出发。
- 3.12 起，`None` 和 -5 到 256 的小整数是永生对象（immortal）：引用计数不再增减，永不释放。

**为什么。** 类型和计数放在对象上，名字才能不带类型、什么都能指。代价是一个大于 256 的整数要 28 字节对象，再加列表里 8 字节的指针，是 C `int` 的 9 倍。

**对应 LeetCode：** 无直接对应的题
