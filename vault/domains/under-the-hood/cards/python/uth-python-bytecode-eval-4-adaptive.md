---
id: uth-python-bytecode-eval-4-adaptive
node: python.bytecode-eval
type: qa
step: 4
---
## Q
**字节码会自己改写：自适应特化**｜Python · CPython 3.11 起

为什么同一段代码调用几次之后，`dis` 里的 `BINARY_OP` 变成了 `BINARY_OP_ADD_INT`？

## A
**背景。** `a + b` 的通用实现要先判断类型：两个 `int`？`float`？字符串？有没有 `__add__`？每次都走一遍很慢。可是同一行代码在实际运行里，类型几乎总是同一种。

**结构。** 解释器对「热」指令做运行时改写（PEP 659 的自适应特化）：指令后面预留几格缓存（inline cache）；执行几次之后，解释器看到两边总是 `int`，就把这条指令原地换成 `BINARY_OP_ADD_INT`，只检查「是不是 `int`」就直接加。哪次传来了 `float`，就退回通用版本，重新计数。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="10" y="30" width="130" height="30" rx="3"/>
<rect x="145" y="30" width="44" height="30" rx="3"/>
<rect x="193" y="30" width="44" height="30" rx="3"/>
<rect x="145" y="130" width="44" height="30" rx="3"/>
<rect x="193" y="130" width="44" height="30" rx="3"/>
<line x1="215" y1="128" x2="215" y2="62" stroke-dasharray="4,3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="10" y="130" width="130" height="30" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="75" y1="60" x2="75" y2="130"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="215.0,62.0 218.0,68.0 212.0,68.0"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="75.0,130.0 72.0,124.0 78.0,124.0"/>
</g>
<g fill="currentColor">
<text x="75" y="49">BINARY_OP +</text>
<text x="167" y="49" font-size="11">缓存</text>
<text x="215" y="49" font-size="11">缓存</text>
<text x="75" y="149" font-size="11">BINARY_OP_ADD_INT</text>
<text x="167" y="149" font-size="11">缓存</text>
<text x="215" y="149" font-size="11">缓存</text>
<text x="170" y="190" font-size="11">先只检查 是不是 int, 再直接相加</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="222" y="96" text-anchor="start" font-size="11">类型变了:</text>
<text x="222" y="112" text-anchor="start" font-size="11">退回通用版</text>
<text x="170" y="15" font-size="11">字节码</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="83" y="90" text-anchor="start" font-size="11">总是 int + int</text>
<text x="83" y="106" text-anchor="start" font-size="11">执行几次后改写</text>
</g>
</g>
</svg>
```

```
# f(a, b) = a * 2 + b，调用 3 次后 dis(f, adaptive=True)
BINARY_OP_MULTIPLY_INT   5 (*)
BINARY_OP_ADD_INT        0 (+)
```

**细节。**

- 实测 3.14.8：函数调用 3 次后，`BINARY_OP` 已变成 `BINARY_OP_MULTIPLY_INT` 和 `BINARY_OP_ADD_INT`，`LOAD_GLOBAL` 变成 `LOAD_GLOBAL_MODULE`。
- 预热门槛很低（源码里 `ADAPTIVE_WARMUP_VALUE` 是 1）；特化失败后，再次尝试前要等的次数每次翻倍，最多约 4095 次。
- 同一机制还有 `LOAD_ATTR_*`、`FOR_ITER_LIST`、`CALL_*` 等一大批特化指令。

**为什么。** 不需要即时编译器（JIT）的编译开销和复杂度，就拿到针对常见类型的快路径；代价是类型总在变的「多态」代码特化不上。

**对应 LeetCode：** 无直接对应的题
