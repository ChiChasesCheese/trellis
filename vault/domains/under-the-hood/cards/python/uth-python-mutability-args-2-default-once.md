---
id: uth-python-mutability-args-2-default-once
node: python.mutability-args
type: qa
step: 2
---
## Q
**默认参数 `[]` 为什么会「记住」上一次**｜Python · CPython 3.14

`def add(x, acc=[]): acc.append(x); return acc`，连着调用 `add(1)` 和 `add(2)`，为什么第二次得到 `[1, 2]`，而不是 `[2]`？

## A
**背景。** 直觉上，默认值像是每次调用时现写的一个空列表。可 Python 里 `def` 是一条会执行的语句：执行它的那一刻才造出函数对象，默认值也在这一刻算好。

**结构。** 函数对象里有个 `__defaults__` 字段（一个元组），`def` 执行时把默认值对象存进去。之后每次调用缺参数，就从元组里取，取到的永远是同一个对象。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<rect x="10" y="28" width="130" height="84" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="75" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">函数对象 add</text>
<rect x="20" y="60" width="110" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="75" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">__defaults__</text>
<rect x="170" y="60" width="40" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="190" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">( )</text>
<line x1="130" y1="73" x2="168" y2="73" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="168.0,73.0 162.0,76.0 162.0,70.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="236" y="60" width="36" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="254" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="272" y="60" width="36" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="290" y="77" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<line x1="210" y1="73" x2="234" y2="73" stroke-width="1.2" stroke="currentColor"/>
<polygon points="234.0,73.0 228.0,76.0 228.0,70.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="272" y="52" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">def 时只造一个列表</text>
<text x="236" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">add(1)</text>
<text x="290" y="128" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">add(2)</text>
<line x1="250" y1="118" x2="252" y2="90" stroke-width="1.2" stroke="currentColor"/>
<polygon points="252.0,90.0 254.6,96.2 248.6,95.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="290" y1="118" x2="290" y2="90" stroke-width="1.2" stroke="currentColor"/>
<polygon points="290.0,90.0 293.0,96.0 287.0,96.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="168" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两次调用拿到的是同一个列表</text>
<text x="170" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">所以结果是 [1, 2]</text>
</svg>
```

**细节。**

- 默认值表达式只在 `def` 执行时求值一次。
- 不可变的默认值（`0`、`None`、字符串）无所谓；可变的 `[]`、`{}` 会被函数一路改下去。
- 外层函数每调用一次，里面的 `def` 就重新执行一次，默认值也重新算一份。

```python
def add(x, acc=[]): acc.append(x); return acc
add(1); add(2)
print(add.__defaults__)  # ([1, 2],)
```

**坑。** 惯用写法是 `acc=None`，函数体里写 `if acc is None: acc = []`。

**对应 LeetCode：** 无直接对应的题
