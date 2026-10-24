---
id: pl-eng-debugging-mechanism-debuginfo
node: engineering.debugging
type: qa
step: 6
---
## Q
调试器是怎样知道“机器码地址对应哪一行源码、哪个变量在哪个寄存器”的？为什么优化过的构建里会看到 `optimized out`，甚至断点位置不对？

## A
**断点的实现**：调试器在目标地址把一条指令暂时替换成一条“陷阱指令”（x86 的 `int3`，ARM64 的 `brk`），CPU 执行到这里触发信号，操作系统通知调试器，进程停住；继续运行前再把原指令换回来。

**从地址到源码**要靠**调试信息**（DWARF 格式），编译时加 `-g` 生成，里面有两张主要的表：
1. **行号表**：机器码地址 → 源文件的第几行；
2. **变量位置表**：变量 → 它在某个地址范围内位于哪个寄存器或栈偏移。

没有调试信息，调试器只看到汇编。Go、Rust 的构建默认会带（或可选），所以发布时去符号（`-s -w`、`strip`）会让调试器和剖析器失去信息。

**优化让映射失真**：优化器把代码重排、内联、展开循环，变量可能被消去、合并到别的值里，或在不同阶段住在不同的寄存器里。实测同一个 Rust 函数，在第 6 行（`t += with_tax;`）设断点，`lldb` 里分别看 debug 与 `-O` 构建：
```
debug:     (unsigned int) with_tax = 15
           (unsigned int) p        = 10
release:   (unsigned int) with_tax = <no location, value may have been optimized out>
           (unsigned int) p        = 20
```
debug 版第一次停下时 `p = 10`，release 版停下时 `p = 20`：循环被重排，“第一次命中”并不是源码里的第一次迭代；`lldb` 也会警告 `compiled with optimization - stepping may behave oddly`。

**Java 和 Python 不受此影响**：JVM 运行优化过的 JIT 代码时可以“去优化”回到解释执行，所以断点永远对应字节码层面的准确位置；Python 的解释器帧保存全部局部变量。

**实践**：
- 调试用 debug 构建；必须调试 release 问题时，开 `debug = true`（Rust 的 `[profile.release] debug = true`）或 Go 的 `-gcflags="all=-N -l"`（关闭优化和内联）；
- 发布时把符号**分离保存**（Rust `split-debuginfo`、Linux 上的 `objcopy --only-keep-debug`），线上二进制可以小，崩溃时仍能用保存的符号还原栈。
