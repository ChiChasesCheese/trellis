---
id: uth-python-attribute-lookup-4-property-cached
node: python.attribute-lookup
type: qa
step: 4
---
## Q
**@property 和 @cached_property 差在哪**｜Python · CPython 3.14

`@property` 每次读都重新计算，`functools.cached_property` 却只算一次。同样是描述符，差在哪？

## A
**背景。** 有时想让 `obj.area` 看起来像个字段，其实背后算出来；有时还想只算一次，之后直接用结果。

**结构。** `property` 是数据描述符，里面存着 `fget`、`fset`、`fdel`，读 `obj.area` 就调用 `fget(obj)`。`cached_property` 只定义了 `__get__`，是非数据描述符：第一次读算出值，写进实例的 `__dict__['area']`；以后再读，实例字典优先于非数据描述符，根本不会再进 `__get__`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<text x="10" y="18" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">property</text>
<rect x="10" y="28" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">obj.p</text>
<line x1="66" y1="40" x2="98" y2="40" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,40.0 92.0,43.0 92.0,37.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="26" width="110" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="155" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">fget(obj)</text>
<text x="226" y="45" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">每次读都算</text>
<line x1="10" y1="78" x2="330" y2="78" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<text x="10" y="98" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" style="fill:var(--accent,#3b6fd4)">cached_property</text>
<rect x="10" y="108" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">obj.q</text>
<line x1="66" y1="120" x2="98" y2="120" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,120.0 92.0,123.0 92.0,117.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="106" width="130" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="165" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">__get__ 算一次</text>
<line x1="230" y1="120" x2="252" y2="120" stroke-width="1.2" stroke="currentColor"/>
<polygon points="252.0,120.0 246.0,123.0 246.0,117.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="254" y="106" width="76" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="292" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">写进字典</text>
<rect x="10" y="152" width="56" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">obj.q</text>
<line x1="66" y1="164" x2="98" y2="164" stroke-width="1.2" stroke="currentColor"/>
<polygon points="98.0,164.0 92.0,167.0 92.0,161.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="100" y="150" width="130" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="165" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">实例字典命中</text>
<text x="240" y="169" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">不再进 __get__</text>
<text x="170" y="204" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">第二次读起 字典先于非数据描述符</text>
</svg>
```

**细节。**

- `property` 没写 setter 也是数据描述符，所以赋值得到 `AttributeError: property 'p' of 'C' object has no setter`。
- `cached_property` 需要实例有 `__dict__`，用了 `__slots__` 的类会抛 `TypeError`。
- 想让缓存失效：`del obj.area`，删掉字典里的值，下次读重新计算。

**为什么。** 「缓存」直接借实例字典实现，命中时不用再进任何函数。

**对应 LeetCode：** 无直接对应的题
