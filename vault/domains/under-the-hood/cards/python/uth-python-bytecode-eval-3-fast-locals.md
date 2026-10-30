---
id: uth-python-bytecode-eval-3-fast-locals
node: python.bytecode-eval
type: qa
step: 3
---
## Q
**局部变量为什么比全局变量快**｜Python · CPython 3.14

`LOAD_FAST` 和 `LOAD_GLOBAL` 差在哪？函数里为什么会出现 `UnboundLocalError`？

## A
**背景。** 变量名在源码里是字符串。如果每次用名字都去字典里查，就要算一次哈希、比较一次，开销大。但一个函数里有哪些局部变量，其实在编译时就能完全确定。

**结构。** 编译器扫描函数体：只要某个名字在函数里被赋值过（参数、`=`、`for` 的循环变量……），它就是局部变量，被编上号放进栈帧里的一个数组，`LOAD_FAST 1` 就是「取数组第 1 格」。其他名字编译成 `LOAD_GLOBAL`，先查模块的全局字典，找不到再查内置字典。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 205">
<g font-size="12" font-family="sans-serif" text-anchor="middle" stroke-width="1.2">
<g fill="none" stroke="currentColor">
<rect x="25" y="34" width="100" height="26" rx="3"/>
<rect x="25" y="90" width="100" height="26" rx="3"/>
<rect x="195" y="34" width="130" height="40" rx="3"/>
<rect x="195" y="90" width="130" height="40" rx="3"/>
<line x1="260" y1="74" x2="260" y2="90" stroke-dasharray="4,3"/>
</g>
<g stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))">
<rect x="25" y="62" width="100" height="26" rx="3"/>
</g>
<g fill="none" style="stroke:var(--accent,#3b6fd4)">
<line x1="138" y1="75" x2="127" y2="75"/>
</g>
<g fill="currentColor" stroke="currentColor" stroke-width="0.5">
<polygon points="260.0,90.0 257.0,84.0 263.0,84.0"/>
</g>
<g stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)">
<polygon points="127.0,75.0 133.0,72.0 133.0,78.0"/>
</g>
<g fill="currentColor">
<text x="75" y="51">[0]  a</text>
<text x="75" y="79">[1]  b</text>
<text x="75" y="107">[2]  c</text>
<text x="260" y="58">globals 字典</text>
<text x="260" y="114">builtins 字典</text>
<text x="170" y="195" font-size="11">局部名编译期定好槽位, 全局名运行时查表</text>
</g>
<g style="fill:var(--dim,#6b7280)">
<text x="75" y="130">数组下标, 一步到位</text>
<text x="260" y="150">先查 globals</text>
<text x="260" y="166">没有再查 builtins</text>
</g>
<g style="fill:var(--accent,#3b6fd4)">
<text x="75" y="20">LOAD_FAST 1</text>
<text x="260" y="20">LOAD_GLOBAL x</text>
</g>
</g>
</svg>
```

**细节。**

- Python 3.11 起，`LOAD_GLOBAL` 会特化成 `LOAD_GLOBAL_MODULE`：缓存全局字典的键版本号和位置，版本号没变就直接读，不再做哈希查找（实测 `dis(f, adaptive=True)` 里能看到）。
- 所以全局访问不再慢得夸张，但仍比数组取值多一步版本校验。

**坑。** 名字只要在函数里**任何位置**被赋值，整个函数里它都是局部变量：先 `print(z)` 再 `z = 1`，会抛 `UnboundLocalError`（3.14 的提示是 `cannot access local variable 'z' where it is not associated with a value`）。

**对应 LeetCode：** 无直接对应的题
