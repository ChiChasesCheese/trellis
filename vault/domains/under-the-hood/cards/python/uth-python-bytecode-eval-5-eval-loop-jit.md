---
id: uth-python-bytecode-eval-5-eval-loop-jit
node: python.bytecode-eval
type: qa
step: 5
---
## Q
**求值循环：分发、尾调用与 JIT**｜Python · CPython 3.14

CPython 主循环的最内层长什么样？3.14 的「尾调用解释器」和 3.13 起的 JIT 各是什么，默认开着吗？

## A
**背景。** 虚拟机的核心就是一个死循环：取一条指令，跳到处理它的那段 C 代码，执行，再取下一条。关键开销在「跳到哪」。经典写法是一个巨大的 `switch`，所有指令共用同一个跳转点，CPU 的分支预测很难猜准下一条是什么。

**结构。** CPython 的主循环（`_PyEval_EvalFrameDefault`）在支持的编译器（GCC、Clang）上默认用「计算跳转」（computed goto）：每条指令的处理代码末尾，自己直接跳向下一条的处理代码，分支预测可以按指令分别学习。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 215">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="8" y="130" width="48" height="26" rx="3"/>
<line x1="32" y1="130" x2="85" y2="80"/>
<rect x="62" y="130" width="48" height="26" rx="3"/>
<line x1="86" y1="130" x2="85" y2="80"/>
<rect x="116" y="130" width="48" height="26" rx="3"/>
<line x1="140" y1="130" x2="85" y2="80"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="45" y="50" width="80" height="28" rx="3"/>
<rect x="180" y="90" width="48" height="26" rx="3"/>
<rect x="234" y="90" width="48" height="26" rx="3"/>
<rect x="288" y="90" width="48" height="26" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="228" y1="103" x2="234" y2="103"/>
<line x1="282" y1="103" x2="288" y2="103"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="85.0,80.0 82.7,86.3 78.6,81.9"/>
<polygon points="85.0,80.0 88.1,85.9 82.1,86.1"/>
<polygon points="85.0,80.0 91.5,81.8 87.4,86.3"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="234.0,103.0 228.0,106.0 228.0,100.0"/>
<polygon points="288.0,103.0 282.0,106.0 282.0,100.0"/>
</g>
<g fill="currentColor">
<text x="85" y="68">switch</text>
<text x="32" y="147" font-size="11">LOAD</text>
<text x="86" y="147" font-size="11">ADD</text>
<text x="140" y="147" font-size="11">STORE</text>
<text x="204" y="107" font-size="11">LOAD</text>
<text x="258" y="107" font-size="11">ADD</text>
<text x="312" y="107" font-size="11">STORE</text>
<text x="170" y="207" font-size="11">分支预测可以按指令分别学习</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="85" y="16">一个 switch</text>
<text x="255" y="16">计算跳转</text>
<text x="85" y="182">都回到同一个跳转点</text>
<text x="255" y="140">每条指令末尾</text>
<text x="255" y="156">直接跳向下一条</text>
</g>
</g>
</svg>
```

**细节。**

- Python 3.14 新增可选的尾调用解释器：每条指令是一个小 C 函数，彼此尾调用。需要 Clang 19 以上，用 `--with-tail-call-interp` 构建；官方文档给出的初步结果是 pyperformance 几何平均快 3% 到 5%。
- 实验性 JIT（3.13 起，PEP 744）：循环热起来之后，把一段字节码转成机器码。3.14 的官方 macOS 和 Windows 二进制里带着它，但默认关闭，设环境变量 `PYTHON_JIT=1` 才打开；官方说法是影响「从慢 10% 到快 20% 不等」，不建议用于生产。

**为什么。** 解释器简单、可移植；JIT 可能更快，但实现复杂，还要权衡预热时间和内存。

**坑。** 尾调用解释器说的是 C 层面的指令跳转，不是 Python 函数的「尾递归优化」；CPython 没有后者。

**对应 LeetCode：** 无直接对应的题
