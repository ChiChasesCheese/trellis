---
id: uth-python-memory-gc-1-refcount
node: python.memory-gc
type: qa
step: 1
---
## Q
**对象什么时候被释放**｜Python · CPython 3.14

Python 怎么知道一个对象没人用了？`del x` 真的释放对象吗？

## A
**背景。** 程序不断创建对象，没人用时必须收回内存。办法之一是定期从变量出发，把能走到的标记出来，走不到的回收，但要扫一遍整个堆。Python 选了更直接的做法：每个对象自己记着「现在有几个地方指着我」。

**结构。** 对象头里有一个引用计数（reference count），多一个引用加 1，少一个减 1，归零立刻释放。例：`a = []` 后计数是 1（`sys.getrefcount` 会再算上函数参数，显示 2）；`b = a` 变 2；`del b` 回到 1。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 180">
<rect x="10" y="30" width="34" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="27" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="10" y="100" width="34" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="27" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b</text>
<rect x="90" y="62" width="66" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="123" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[ ]</text>
<text x="123" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">计数 2</text>
<line x1="44" y1="42" x2="90" y2="72" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,72.0 83.3,71.2 86.6,66.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="44" y1="112" x2="90" y2="96" stroke-width="1.2" stroke="currentColor"/>
<polygon points="90.0,96.0 85.3,100.8 83.3,95.1" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="190" y="30" width="34" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="207" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a</text>
<rect x="190" y="100" width="34" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="207" y="116" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">b</text>
<rect x="270" y="62" width="66" height="44" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="303" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">[ ]</text>
<text x="303" y="98" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">计数 1</text>
<line x1="224" y1="42" x2="270" y2="72" stroke-width="1.2" stroke="currentColor"/>
<polygon points="270.0,72.0 263.3,71.2 266.6,66.2" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="224" y1="112" x2="270" y2="96" stroke-width="1.2" stroke="currentColor" stroke-dasharray="4 3"/>
<line x1="234" y1="100" x2="248" y2="116" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="248" y1="100" x2="234" y2="116" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="172" y="76" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">del b</text>
<line x1="160" y1="86" x2="186" y2="86" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="186.0,86.0 180.0,89.0 180.0,83.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="170" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">计数归零的那一刻立刻释放</text>
</svg>
```

**细节。**

- 实测 `sys.getrefcount(a)`：`a = []` 后是 2，`b = a` 变 3，`del b` 回到 2。
- `del x` 只删掉名字，减一次计数；还有别的引用，对象就还在。
- 释放是确定性的，不用等扫描，`__del__` 也立刻执行。

**为什么。** 释放时机可预测、没有 GC 暂停；代价是每次赋值都要改计数，而且处理不了循环引用。

**对应 LeetCode：** 无直接对应的题
