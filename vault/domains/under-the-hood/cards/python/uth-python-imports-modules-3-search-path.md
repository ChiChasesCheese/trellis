---
id: uth-python-imports-modules-3-search-path
node: python.imports-modules
type: qa
step: 3
---
## Q
**import 去哪里找文件**｜Python · CPython 3.14

项目里放了一个 `random.py`，`import random` 为什么拿到的是它，而不是标准库的？Python 按什么顺序找模块？

## A
**背景。** 同名模块可能躺在好几个目录里（标准库、第三方、自己写的），需要一个固定的先后顺序：谁排前面就用谁。

**结构。** 先查 `sys.modules` 缓存；没有，再按顺序问三位「找人的」（`sys.meta_path`）：内置模块、冻结模块（启动必需的核心模块，如 `os`，字节码已编译进解释器），最后是 `PathFinder`，沿 `sys.path` 这个目录列表从前往后找，第一个命中就停。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 190">
<rect x="14" y="18" width="204" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="24" y="37" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">1  脚本所在目录 有 random.py</text>
<rect x="14" y="54" width="204" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="24" y="73" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">2  PYTHONPATH</text>
<rect x="14" y="90" width="204" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="24" y="109" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">3  标准库 有 random.py</text>
<rect x="14" y="126" width="204" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="24" y="145" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">4  site-packages</text>
<line x1="246" y1="24" x2="246.0" y2="140.0" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="246,146 243.0,140.0 249.0,140.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="258" y="70" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">从上往下</text>
<text x="258" y="88" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">第一个命中</text>
<text x="258" y="106" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">就停</text>
<text x="170" y="176" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">内置模块 如 sys 在查 sys.path 之前就命中</text>
</svg>
```

**细节。**

- `python script.py` 会把脚本所在目录放在 `sys.path` 最前面；`python -m pkg.mod` 放的是当前目录。
- `python -P`（3.11 起）或环境变量 `PYTHONSAFEPATH` 可以去掉这个自动加入的目录。

**坑。** 自己的 `random.py`、`logging.py` 会遮蔽标准库。3.13 起，报错会提示 `consider renaming ... since it has the same name as the standard library module`。

**对应 LeetCode：** 无直接对应的题
