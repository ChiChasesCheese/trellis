---
id: uth-python-bytecode-eval-2-code-object-pyc
node: python.bytecode-eval
type: qa
step: 2
---
## Q
**编译结果存在哪：code object 与 .pyc**｜Python · CPython 3.14

函数的字节码放在哪个对象里？为什么同一个模块被多次启动，只需要编译一次？

## A
**背景。** 光有指令不够：`LOAD_FAST 0` 里的 0 是第几个变量？常量 2 存在哪？编译的产物还得带上这些表。

**结构。** 每个函数、模块、类体编译后得到一个代码对象（code object），`f.__code__` 就是它。它里面有：`co_code`（指令序列）、`co_consts`（常量表）、`co_varnames`（局部变量名）、`co_stacksize`（操作数栈最深有多少格，提前算好）。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 235">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="8" y="40" width="60" height="30" rx="3"/>
<rect x="100" y="10" width="150" height="100" rx="3"/>
<line x1="230" y1="148" x2="230" y2="112" stroke-dasharray="4,3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="70" y="150" width="200" height="30" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="68" y1="55" x2="98" y2="55"/>
<line x1="150" y1="112" x2="150" y2="148"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="230.0,112.0 233.0,118.0 227.0,118.0"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="98.0,55.0 92.0,58.0 92.0,52.0"/>
<polygon points="150.0,148.0 147.0,142.0 153.0,142.0"/>
</g>
<g fill="currentColor">
<text x="38" y="59">x.py</text>
<text x="112" y="50" text-anchor="start" font-size="11">co_code  指令</text>
<text x="112" y="66" text-anchor="start" font-size="11">co_consts  常量</text>
<text x="112" y="82" text-anchor="start" font-size="11">co_varnames  局部名</text>
<text x="112" y="98" text-anchor="start" font-size="11">co_stacksize  栈深</text>
<text x="170" y="169" font-size="11">__pycache__/x.cpython-314.pyc</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="238" y="135" text-anchor="start" font-size="11">再 import</text>
<text x="170" y="202">源文件修改时间没变: 直接读 .pyc</text>
<text x="170" y="222">只省下编译, 不会让运行变快</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="83" y="45" font-size="11">编译</text>
<text x="175" y="28">code object</text>
<text x="158" y="135" text-anchor="start" font-size="11">写入缓存</text>
</g>
</g>
</svg>
```

**细节。**

- 实测 `f(a, b): return a * 2 + b` 的 `co_consts` 是 `(2,)`，`co_varnames` 是 `('a', 'b')`，`co_stacksize` 是 `2`。
- 缓存文件名里带解释器版本：`importlib.util.cache_from_source("x.py")` 得到 `__pycache__/x.cpython-314.pyc`。
- 默认靠比较源文件的修改时间判断缓存过没过期；直接从命令行运行的主脚本不会被缓存。

**为什么。** 把「解析源码」这一步从每次启动里省掉；文件名带版本，多个 Python 版本互不干扰。注意 `.pyc` 只让**加载**变快，运行速度不变。

**对应 LeetCode：** 无直接对应的题
