---
id: uth-python-imports-modules-1-import-once
node: python.imports-modules
type: qa
step: 1
---
## Q
**import 到底做了什么**｜Python · CPython 3.14

两个文件都 `import b`，`b.py` 里的 `print` 会执行几次？`import` 背后做了什么？

## A
**背景。** 代码拆在多个文件里，`a.py` 想用 `b.py` 的函数。最笨的办法，是把 `b.py` 的内容粘进每个用到它的文件：每处都重复一份、重复执行。

**结构。** `import b` 做三步：先查 `sys.modules`（一个 `dict`：模块名 → 模块对象），有就直接用；没有就按 `sys.path` 找到 `b.py`，造一个空模块对象并**先登记进 `sys.modules`**；最后在这个模块里把 `b.py` 从头执行一遍。所以 `b.py` 的顶层代码只跑一次，之后的 `import b` 都只是查表。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 214">
<rect x="125" y="6" width="90" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="24" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">import b</text>
<rect x="90" y="46" width="160" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b 在 sys.modules 里?</text>
<line x1="170" y1="32" x2="170.0" y2="40.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,46 167.0,40.0 173.0,40.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<line x1="250" y1="60" x2="260.0" y2="60.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="266,60 260.0,63.0 260.0,57.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="266" y="46" width="66" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="299" y="64" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">直接用</text>
<text x="258" y="42" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">有</text>
<line x1="170" y1="74" x2="170.0" y2="86.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,92 167.0,86.0 173.0,86.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<text x="180" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没有</text>
<rect x="80" y="92" width="180" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="110" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">按 sys.path 找到 b.py</text>
<line x1="170" y1="118" x2="170.0" y2="126.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,132 167.0,126.0 173.0,126.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="50" y="132" width="240" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="150" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">造空模块 先登记进 sys.modules</text>
<line x1="170" y1="158" x2="170.0" y2="166.0" stroke-width="1.2" stroke="currentColor"/>
<polygon points="170,172 167.0,166.0 173.0,166.0" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
<rect x="80" y="172" width="180" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="170" y="190" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">在模块里从头执行 b.py</text>
</svg>
```

**细节。**

- 执行到一半报错，登记会被删掉，下次 `import` 从头再来。
- 找到源文件后，先看 `__pycache__/b.cpython-314.pyc`（编译好的字节码），源文件的修改时间和大小对得上就跳过编译；直接运行的入口脚本不走这个缓存。

**对应 LeetCode：** 无直接对应的题
