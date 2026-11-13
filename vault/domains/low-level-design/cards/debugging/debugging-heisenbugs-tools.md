---
id: debugging-heisenbugs-tools
node: debugging.heisenbugs
type: qa
step: 3
---
## Q
一个 C++ 服务在高并发下偶尔崩溃，Python 测试框架偶尔卡住，都很难复现。有哪些不依赖「运气好正好碰上」的工具？各自抓什么、代价多大？

## A
**用工具去检测问题的条件（数据竞争、内存错误），或者把一次真实的执行录下来反复回放，而不是等它在调试器底下再发生一次。**

- **ThreadSanitizer（TSan）：** 编译时加 `-fsanitize=thread -g`，运行时检测数据竞争：两个线程无同步地访问同一内存、且至少一个是写。它报告两边的调用栈，即使这一次并没有真的算错。代价是运行时间慢几倍到十几倍、内存多几倍。
- **AddressSanitizer（ASan）：** `-fsanitize=address`，抓越界、释放后使用（use-after-free）、重复释放，大约慢 2 倍。很多「偶尔崩溃」其实是内存被悄悄写坏了，ASan 让它在第一次写坏时就报错。
- **录制回放（`rr`，Linux）：** `rr record ./server` 录下一次执行，`rr replay` 每次回放都完全一样，还能反向执行（`reverse-continue`），从崩溃点往回找是谁写坏了数据。`rr record --chaos` 会随机调整线程调度，帮助触发罕见的交错顺序。
- **崩溃现场：** 打开 core dump（`ulimit -c unlimited`），崩溃后用 `gdb ./server core` 看所有线程的栈（`thread apply all bt`）。
- **Python 卡住：** `py-spy dump --pid <pid>` 不停下进程就能打印所有线程当前的栈；`faulthandler.dump_traceback_later(600)` 让测试在 600 秒后自动打印栈；`PYTHONDEVMODE=1` 打开额外的运行时检查。
- **日志：** 写入内存里的环形缓冲区（ring buffer），出错时再导出最近的 N 条，比到处 `print` 对时序的影响小得多。
- **用法建议：** 在 CI 里定期用 TSan/ASan 构建跑一遍并发和压力测试，把检测从「出事后排查」变成「出事前发现」。
