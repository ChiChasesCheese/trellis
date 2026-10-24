---
id: pl-foundations-execution-models-principle
node: foundations.execution-models
type: qa
step: 1
---
## Q
CPU 只能执行机器码，而程序员写的是源代码。语言要用什么方式弥合这个差距？有哪几种执行模型（execution model）？

## A
问题：CPU 只认特定指令集（比如 x86-64 或 ARM64）的二进制指令，源代码是人读的文本。必须有一个翻译步骤，区别只在「翻译什么时候做、翻译成什么」。

三种基本做法：

1. 提前编译（AOT，ahead-of-time compilation）：运行前一次性翻译成目标机器的机器码，交付的是可直接执行的文件。运行时没有翻译开销，但产物绑定 CPU 和操作系统。
2. 字节码加虚拟机（bytecode + virtual machine）：先编译成与具体 CPU 无关的中间指令（字节码），再由虚拟机在运行时执行。虚拟机还可以把热点字节码即时编译（JIT，just-in-time compilation）成机器码。
3. 解释执行（interpretation）：运行时逐条读取程序（语法树或字节码）并直接做它要求的事，不生成机器码。实现最简单，启动最快，运行最慢。

一句话定位：C++、Go 和 Rust 走第 1 条；Java 走第 2 条；CPython 先把源码编译成字节码，再用解释器逐条执行，属于第 3 条。实际系统常常混合：Java 先解释再 JIT，是 2 和 3 的叠加。
