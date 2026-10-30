---
id: uth-python-imports-modules-4-circular
node: python.imports-modules
type: qa
step: 4
---
## Q
**循环导入为什么拿到半成品**｜Python · CPython 3.14

`a.py` 开头 `from b import fb`，`b.py` 开头 `from a import fa`。运行 `import a` 会怎样，为什么？

## A
**背景。** 模块 a 要用 b，b 又要用 a。如果必须等一个完整执行完才能交给另一个，就会互相死等。Python 的做法是：模块先登记进 `sys.modules` 再执行，所以 b 遇到 a 时，拿到的是「还没执行完」的 a。

**结构。** `from a import fa` 要在模块 a 里取名字 `fa`。a 还停在第 1 行，`def fa` 没执行，取不到，就抛 `ImportError`。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 216">
<text x="80" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">a.py</text>
<text x="260" y="16" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">b.py</text>
<rect x="10" y="26" width="140" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="80" y="46" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">from b import fb</text>
<rect x="10" y="62" width="140" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="80" y="82" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">def fa(): ...</text>
<rect x="190" y="104" width="140" height="30" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="260" y="124" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">from a import fa</text>
<rect x="190" y="140" width="140" height="30" rx="3" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
<text x="260" y="160" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">def fb(): ...</text>
<line x1="150" y1="46" x2="186.9" y2="106.9" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="190,112 184.3,108.4 189.5,105.3" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="176" y="74" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<line x1="190" y1="126" x2="153.9" y2="84.5" stroke-width="1.2" stroke-dasharray="4 3" stroke="currentColor"/>
<polygon points="150,80 156.2,82.6 151.7,86.5" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="158" y="112" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">2</text>
<text x="14" y="190" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1 import a: 登记 a, 执行第 1 行, 去导入 b</text>
<text x="14" y="208" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">2 b 要 a 的 fa, a 还没执行到 def: 报错</text>
</svg>
```

**细节。**

- 报错写的是 `cannot import name 'fa' from partially initialized module 'a'`，括号里还提示 `most likely due to a circular import`。
- 换个入口结果不同：先 `import b`，报的就是 `fb` 取不到。
- 只写 `import a`（只绑定模块对象，不取名字），导入本身不会失败；等真正调用 `a.fa()` 时，a 早已执行完。
- 解法：把共用的部分抽到第三个模块；或把 `import` 挪进函数里，用到时才导入。

**对应 LeetCode：** 无直接对应的题
