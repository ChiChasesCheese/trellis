---
id: pl-eng-debugging-found-debugger
node: engineering.debugging
type: qa
step: 2
---
## Q
交互式调试器在 Go、Java、Rust、Python 里分别是什么？断点停下来之后能看到什么，一个 Python 的 `pdb` 会话是什么样子？

## A
断点调试的流程在所有语言里相同：在某一行设断点 → 运行 → 程序停在那一行 → 查看变量和调用栈 → 单步或继续。区别在于**谁来实现**：

| 语言 | 常用调试器 | 说明 |
|---|---|---|
| Go | Delve（`dlv`） | 理解 goroutine：可以列出所有 goroutine 并切换；普通的 gdb 对 Go 的运行时结构不友好 |
| Java | IDE（IntelliJ 等），底层是 JDWP（Java Debug Wire Protocol） | 调试器通过协议连到 JVM，JVM 自己提供断点、变量、线程；可远程附加到 `-agentlib:jdwp=...` 启动的进程 |
| Rust | `lldb`/`gdb`（常用 `rust-lldb`、IDE 的 CodeLLDB） | 把机器码当原生程序调试，依赖 `-g` 的调试信息；泛型、闭包名称较难读 |
| Python | `pdb`（内置）、IDE | 解释器自带；`breakpoint()` 一行即可在代码里设断点 |

Python 的会话（脚本化输入），程序 `total` 函数里循环累加价格：
```
(Pdb) b 4                  # breakpoint at line 4
(Pdb) c                    # continue
> pd.py(4)total()
-> t += p * (1 + tax)
(Pdb) p p, t               # print variables
(10, 0)
(Pdb) bt                   # call stack
  pd.py(7)<module>()
> pd.py(4)total()
```
停在第一次进入循环时：`p = 10`，`t = 0`。

**设计差异的原因**：Python 和 Java 的运行时自己持有全部程序结构（解释器的帧、JVM 的栈），所以调试器可以通过运行时提供的接口直接读取，非常准确；Go 和 Rust 编译成机器码，调试器只能靠**调试信息**（DWARF，一种描述“机器地址对应哪行源码、哪个寄存器存哪个变量”的数据）去反推，这使得优化过的代码很难调：优化会让这种映射失真。

**资深工程师的习惯**：不要在线上进程挂调试器；复现之后用测试把它固定下来，在本地用调试器看；平时更多靠日志和断言。
