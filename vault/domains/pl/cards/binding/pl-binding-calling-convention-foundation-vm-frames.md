---
id: pl-binding-calling-convention-foundation-vm-frames
node: binding.calling-convention
type: qa
step: 5
---
## Q
Java 和 Python 的函数调用在虚拟机里是什么样的？它们的「栈帧」和 Rust、Go 的机器栈帧有什么不同？

## A
Java 和 Python 的代码先编译成**字节码**，由虚拟机执行。字节码没有寄存器的概念，是一种**基于操作数栈**的指令集：指令把值压入一个栈，运算指令弹出操作数、压回结果。

Java 的一个方法 `add3(a, b, c)` 和它的调用者编译后是：

```text
add3:   iload_0  iload_1  iload_2  imul  iadd  ireturn
caller: iload_0  iconst_2 iconst_3 invokestatic add3
        iload_0  iconst_4 iconst_5 invokestatic add3  iadd  ireturn
```

每个被调用的方法在 JVM 里得到一个**帧**：包含**局部变量表**（参数就是前几个槽，`iload_0` 读第 0 槽）和**操作数栈**。调用者把实参压入自己的操作数栈，`invokestatic` 把它们移进新帧的局部变量表，返回值回到调用者的操作数栈。这套约定属于 JVM，与 CPU 无关，所以字节码可以跨平台。

JVM 解释执行时用这种帧；方法被 JIT 编译后，帧变成真正的机器栈帧，参数用寄存器，热点方法还会被内联，帧干脆消失。因此 Java 的调用成本在热点上与 C 接近。

Python 的字节码也基于栈（`LOAD_FAST`、`CALL`）。每次调用创建一个**帧对象**，保存局部变量和值栈。Python 3.11 起，纯 Python 函数之间的调用不再占用 C 语言栈，帧在解释器自己管理的数据栈里分配，所以调用比以前便宜，但仍明显慢于编译语言：参数要打包、帧要初始化。

关键差异：

1. **谁管栈**：C++、Rust、Go 是原生栈，由 CPU 的栈指针和 ABI 管理；Java、Python 是虚拟机栈，由运行时管理。
2. **栈大小的上限**：JVM 线程栈由 `-Xss` 设定（几百 KB 到几 MB）；Python 另设一个递归深度上限 `sys.getrecursionlimit()`，默认 1000。
3. **能否被观察**：虚拟机栈帧里的信息是结构化的，所以异常堆栈、调试器、`sys._getframe` 能直接读，原生栈需要调试符号。
