---
id: uth-python-bytecode-eval-1-compile-run
node: python.bytecode-eval
type: qa
step: 1
---
## Q
**Python 怎么跑起来：字节码与栈式虚拟机**｜Python · CPython 3.14

`a * 2 + b` 在 CPython 里是怎么被执行的？`dis` 打印出来的是什么？

## A
**背景。** CPU 只认机器码。有两个极端做法：每次运行都逐行读源码、边解析边执行，太慢，循环里同一行要被反复解析；或者像 C 那样提前为每个平台编译成机器码。CPython 取中间：先把源码一次性翻译成一串紧凑的、与平台无关的「虚拟指令」，叫字节码（bytecode），再由一个 C 写的程序（虚拟机）逐条执行。

**结构。** 虚拟机是栈式的：每条指令从一个「操作数栈」里取数，再把结果放回去。用 `dis.dis(f)` 可以把字节码打印出来。以 `a = 3, b = 4` 为例，栈里一步步是这样的：

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 185">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="8" y="72" width="56" height="26" rx="3" stroke-dasharray="4,3"/>
<rect x="8" y="44" width="56" height="26" rx="3" stroke-dasharray="4,3"/>
<rect x="74" y="100" width="56" height="26" rx="3"/>
<rect x="74" y="44" width="56" height="26" rx="3" stroke-dasharray="4,3"/>
<rect x="140" y="72" width="56" height="26" rx="3" stroke-dasharray="4,3"/>
<rect x="140" y="44" width="56" height="26" rx="3" stroke-dasharray="4,3"/>
<rect x="206" y="100" width="56" height="26" rx="3"/>
<rect x="206" y="44" width="56" height="26" rx="3" stroke-dasharray="4,3"/>
<rect x="272" y="72" width="56" height="26" rx="3" stroke-dasharray="4,3"/>
<rect x="272" y="44" width="56" height="26" rx="3" stroke-dasharray="4,3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="8" y="100" width="56" height="26" rx="3"/>
<rect x="74" y="72" width="56" height="26" rx="3"/>
<rect x="140" y="100" width="56" height="26" rx="3"/>
<rect x="206" y="72" width="56" height="26" rx="3"/>
<rect x="272" y="100" width="56" height="26" rx="3"/>
</g>
<g fill="currentColor">
<text x="36" y="117">3</text>
<text x="102" y="117">3</text>
<text x="102" y="89">2</text>
<text x="168" y="117">6</text>
<text x="234" y="117">6</text>
<text x="234" y="89">4</text>
<text x="300" y="117">10</text>
<text x="170" y="170">a * 2 + b  =&gt;  10</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="170" y="150">a = 3, b = 4, 栈底在下</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="36" y="24">LOAD a</text>
<text x="102" y="24">LOAD 2</text>
<text x="168" y="24">*</text>
<text x="234" y="24">LOAD b</text>
<text x="300" y="24">+</text>
</g>
</g>
</svg>
```

```
LOAD_FAST_BORROW   0 (a)
LOAD_SMALL_INT     2
BINARY_OP          5 (*)
LOAD_FAST_BORROW   1 (b)
BINARY_OP          0 (+)
RETURN_VALUE
```

**细节。**

- 每条指令占 2 字节：一个操作码加一个参数，参数多半是「第几个局部变量或常量」的下标。
- 字节码不跨版本通用，指令名也随版本变：上面的 `LOAD_SMALL_INT` 是 3.14 新增的。

**为什么。** 编译一次、执行多次，且同一份字节码在所有平台上都能跑；代价是每条指令都要经过一次「取指令、分发、执行」的循环，比直接跑机器码慢。

**对应 LeetCode：** 无直接对应的题
