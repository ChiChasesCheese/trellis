---
id: uth-python-scope-closures-5-fast-locals
node: python.scope-closures
type: qa
step: 5
---
## Q
**同样的循环，放进函数里为什么更快**｜Python · CPython 3.14

同一段 200 万次的循环，从脚本顶层挪进函数里，为什么快了将近一倍？

## A
**背景。** 模块顶层的变量是全局变量，放在一个字典里：每次读写 `s`、`i`，都要拿名字去字典里查。函数里的局部变量不一样。

**结构。** 函数的局部变量放在栈帧里的一个数组，编译时每个名字就分好了下标，运行时按下标取，不查字典。字节码里对应 `LOAD_FAST` 和 `STORE_FAST`；模块顶层则是 `LOAD_NAME` 和 `STORE_NAME`，按名字查字典。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 200">
<text x="10" y="20" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2000000 次循环 CPython 3.14.8 实测</text>
<text x="10" y="50" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">模块级  LOAD_NAME 查字典</text>
<rect x="10" y="58" width="222" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="240" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">44.5 ms</text>
<text x="10" y="118" text-anchor="start" font-size="12" font-family="sans-serif" fill="currentColor">函数内  LOAD_FAST 按下标取</text>
<rect x="10" y="126" width="115" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="133" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">23.1 ms</text>
<text x="170" y="188" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">同样的循环 快了约 1.9 倍</text>
</svg>
```

**细节。**

- 实测（CPython 3.14.8，`for i in range(2_000_000): s += i`）：顶层 44.5 ms，函数内 23.1 ms。
- 题解写在 `class Solution` 的方法里，变量本来就是局部变量，不吃这个亏。
- 局部变量的名字必须在编译时确定，这正是「赋值即局部」那条规则的由来。

**为什么。** 编译时定好每个局部变量的位置，运行时就少一次字典查找。

**对应 LeetCode：** 无直接对应的题
