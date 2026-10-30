---
id: uth-python-objects-names-1-labels
node: python.objects-names
type: qa
step: 1
---
## Q
**变量是盒子还是标签**｜Python · CPython 3.14

`a = [1, 2]`、`b = a`，再 `b.append(3)`，为什么 `a` 也变成了 `[1, 2, 3]`？`b = a` 到底复制了什么？

## A
**背景。** C 里的变量是一只盒子，值装在盒子里，`b = a` 把值抄进另一只盒子。Python 的值大小不一（列表、字符串、函数都有），塞不进固定大小的盒子，于是反过来：值各自放在堆（heap，运行时动态申请的内存）上，叫对象；变量只是一个名字，指着某个对象。

**结构。** 名字 → 对象的指针表，模块级的名字就存在一个 `dict` 里（`globals()`）。`b = a` 只是在表里再添一条「`b` → 同一个对象」，不复制任何东西。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="130" y="24" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">b = a  同一个对象</text>
<rect x="12" y="36" width="34" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="29" y="51" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="12" y="70" width="34" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="29" y="85" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="130" y="40" width="36" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="148" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="166" y="40" width="36" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="184" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="202" y="40" width="36" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="220" y="58" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<text x="246" y="58" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">append(3)</text>
<line x1="46" y1="47" x2="128" y2="52" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.0,52.0 121.8,54.6 122.2,48.6" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="46" y1="81" x2="128" y2="58" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.0,58.0 123.0,62.5 121.4,56.7" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="130" y="118" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">c = a.copy()  新对象</text>
<rect x="12" y="132" width="34" height="22" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="29" y="147" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c</text>
<rect x="130" y="126" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="148" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="166" y="126" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="184" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<rect x="202" y="126" width="36" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="220" y="144" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<line x1="46" y1="143" x2="128" y2="140" stroke-width="1.2" stroke="currentColor"/>
<polygon points="128.0,140.0 122.1,143.2 121.9,137.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="170" y="184" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">赋值只贴标签 copy() 才造新对象</text>
</svg>
```

**细节。**

- `b.append(3)` 改的是对象本身，所有指着它的名字都看得到；`id(a) == id(b)` 为真（CPython 里 `id()` 就是对象的内存地址）。
- `a = [9]` 是把 `a` 这张标签撕下来贴到新对象上，`b` 不受影响。
- 要独立副本，得显式造新对象：`a.copy()`。

**为什么。** 名字不带类型，也不占固定大小，一个名字可以先后指向任何对象。代价是「以为复制了」的别名陷阱。

**对应 LeetCode：** 无直接对应的题
