---
id: uth-python-exceptions-context-2-zero-cost
node: python.exceptions-context
type: qa
step: 2
---
## Q
**try 为什么不花钱**｜Python · CPython 3.11 起

循环里套一层 `try`，没出错时会变慢吗？出错时，解释器怎样知道该跳到哪个 `except`？

## A
**背景。** 直觉做法是：进入 `try` 时先登记「出错就回这里」，离开时再撤销，每次进入都要付一次，哪怕一辈子不出错。CPython 3.10 及更早就是这样，要执行一条 `SETUP_FINALLY` 指令。

**结构。** 3.11 起改成编译时记账：编译器把「哪一段字节码（解释器执行的指令序列）归哪个 `except` 管」写成一张表，存在函数的 `co_exceptiontable` 里。`try` 本身不再生成登记指令，没出错时解释器根本不看这张表；出错时才查表，找到处理者就跳过去，找不到就去调用者的帧里再查。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 176">
<text x="16" y="16" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">字节码 从左到右</text>
<rect x="16" y="26" width="64" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="48.0" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">LOAD g</text>
<rect x="84" y="26" width="50" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="109.0" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">CALL</text>
<rect x="138" y="26" width="64" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="170.0" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">POP_TOP</text>
<rect x="212" y="26" width="70" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="247" y="45" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">return 2</text>
<line x1="16" y1="64" x2="202" y2="64" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="16" y1="60" x2="16" y2="68" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="202" y1="60" x2="202" y2="68" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="109" y="84" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">表项: 这一段 归 L3 处理</text>
<line x1="109" y1="92" x2="109.0" y2="106.0" stroke-width="1.2" stroke-dasharray="4 3" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="109,112 106.0,106.0 112.0,106.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<rect x="24" y="114" width="170" height="28" rx="3" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="109" y="133" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">L3  except KeyError</text>
<text x="170" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">没出错不看表 出错才查表</text>
</svg>
```

```python
def f():
    try:
        g()
    except KeyError:
        return 1
    return 2
```

**细节。**

- `dis.dis(f)` 末尾能看到表项 `L1 to L2 -> L3`：只有 `g()` 的那几条指令被标在表里。
- 每项记三件事：覆盖哪一段指令、处理者在哪、运算栈要退回多深；表按位置排序，很长时先二分再逐项扫。

**为什么。** 绝大多数调用不出错，所以让成功路径零成本，把代价转给失败路径：要查表、建异常对象、记回溯，比普通 `return` 贵。「通常成功、偶尔失败」的场合适合用异常。

**对应 LeetCode：** 无直接对应的题
