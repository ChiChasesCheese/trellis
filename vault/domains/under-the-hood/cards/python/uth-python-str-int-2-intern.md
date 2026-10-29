---
id: uth-python-str-int-2-intern
node: python.str-int
type: qa
step: 2
---
## Q
**is 为什么有时对、有时错**｜Python · CPython 3.14

`int('256') is int('256')` 为 `True`，`int('257') is int('257')` 为 `False`；字符串也有类似现象，这是怎么回事？

## A
**背景。** `==` 比的是值，`is` 比的是「是不是同一个对象」。小整数、短名字用得极多，每次新建一个太浪费，所以解释器预先建好一批共享。

**结构。** 预先建好并共享的不可变对象：小整数缓存 -5 到 256，以及驻留（interning）字符串表，里面每个字符串只存一份。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="20" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">256 在缓存范围内</text>
<rect x="20" y="28" width="36" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="44" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">x</text>
<rect x="20" y="62" width="36" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="78" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">y</text>
<rect x="150" y="44" width="56" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="178" y="61" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">256</text>
<line x1="56" y1="40" x2="150" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,52.0 143.7,54.2 144.4,48.3" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="56" y1="74" x2="150" y2="62" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,62.0 144.4,65.7 143.7,59.8" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="222" y="61" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">is 为 True</text>
<text x="20" y="122" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">257 超出范围</text>
<rect x="20" y="134" width="36" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">x</text>
<rect x="20" y="168" width="36" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="38" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">y</text>
<rect x="150" y="134" width="56" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="178" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">257</text>
<rect x="150" y="168" width="56" height="24" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="178" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">257</text>
<line x1="56" y1="146" x2="150" y2="146" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,146.0 144.0,149.0 144.0,143.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="56" y1="180" x2="150" y2="180" stroke-width="1.2" stroke="currentColor"/>
<polygon points="150.0,180.0 144.0,183.0 144.0,177.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="222" y="166" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">is 为 False</text>
</svg>
```

**细节。**

- 实测 `int('-5') is int('-5')` 为真，`int('-6') is int('-6')` 为假。
- 运行时拼出的 `'hello_world'` 与字面量不是同一个对象；`sys.intern` 后才相同。
- 标识符、属性名自动驻留。

**为什么。** 驻留后 `dict` 查属性名时，哈希相同再比一次指针就够，不用逐字符比较。

**坑。** 比较值永远用 `==`，`is` 只用于 `None`。

**对应 LeetCode：** 无直接对应的题
