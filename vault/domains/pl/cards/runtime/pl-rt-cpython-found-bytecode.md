---
id: pl-rt-cpython-found-bytecode
node: runtime.cpython-internals
type: qa
step: 2
---
## Q
CPython 的字节码和求值循环（eval loop）是什么？怎样用 `dis` 看一个循环被编译成了什么，它是怎样一条条执行的？

## A
CPython 执行 Python 代码分两步：先把函数编译成**字节码**（一个字节序列，每条指令一个操作码加可选参数，存放在函数的 `__code__` 里），再由 C 写的**求值循环**逐条执行。字节码是基于栈的：指令操作一个值栈和一组局部变量槽。

用标准库 `dis` 可以看到：
```python
def loop(n):
    s = 0
    for i in range(n):
        s += i
    return s
dis.dis(loop)
```
核心部分的输出（节选）：
```
LOAD_SMALL_INT           0
STORE_FAST               1 (s)
...
GET_ITER
FOR_ITER                 (to END)
STORE_FAST               2 (i)
LOAD_FAST_BORROW_LOAD_FAST_BORROW  (s, i)
BINARY_OP                13 (+=)
STORE_FAST               1 (s)
JUMP_BACKWARD            (to FOR_ITER)
```
读法：`LOAD_FAST`/`STORE_FAST` 读写局部变量槽（按下标，很快）；`FOR_ITER` 向迭代器要下一个值，耗尽就跳出；`BINARY_OP` 弹出栈顶两个值做加法；`JUMP_BACKWARD` 回到循环头。每次迭代执行大约 5 到 6 条字节码。

**求值循环**本质上是一个巨大的 `switch`（实际用“计算跳转”或尾调用优化）：

```
while (true) {
    opcode = *next_instr++;
    switch (opcode) { case BINARY_OP: ...; case STORE_FAST: ...; }
}
```
每条字节码一次取指、一次分派、一次对应的 C 代码执行。这就是“解释开销”：每条指令的执行除了真正的工作，还有分派的成本。

两个要点：
1. 字节码是**实现细节**，随版本变化（3.11 加入特化指令，3.13、3.14 又引入新指令）；`.pyc` 文件就是缓存的字节码，不同版本不能通用；
2. 函数内的局部变量走 `LOAD_FAST`（下标），全局变量走字典查找，这是函数内代码更快的原因。
