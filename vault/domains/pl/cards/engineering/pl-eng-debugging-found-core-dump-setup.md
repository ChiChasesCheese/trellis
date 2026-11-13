---
id: pl-eng-debugging-found-core-dump-setup
node: engineering.debugging
type: qa
step: 11
---
## Q
一个 C++ 写的服务（或带原生扩展的 Python 进程）在测试机上偶尔崩溃，退出码是 `-11`（段错误，SIGSEGV），日志里什么都没有。怎么确保下次崩溃时留下核心转储（core dump）？它存到哪里，怎么找到？

## A
**核心转储是进程被致命信号杀死那一刻的内存镜像，加上每个线程的寄存器。有了它和对应的可执行文件、调试符号，就能在事后用调试器看到崩溃时的调用栈和变量。默认常常不生成，要先打开。**

**三个开关**：
1. **大小限制：** `ulimit -c unlimited`（只对当前 shell 和它启动的进程有效）；systemd 服务写 `LimitCORE=infinity`；容器里 `docker run --ulimit core=-1`。默认的 `0` 表示不写。
2. **写到哪里：** 由内核参数 `/proc/sys/kernel/core_pattern` 决定，它对整台机器生效，容器里改不了，要在宿主机上配。
   - 以文件路径开头，例如 `/var/crash/core.%e.%p.%t`：程序名、PID、时间戳。
   - 以 `|` 开头，表示交给一个程序处理。很多发行版是 `|/usr/lib/systemd/systemd-coredump ...`，转储被收进日志系统，用 `coredumpctl list` 查看，`coredumpctl gdb <PID>` 直接用 gdb 打开。
3. **调试符号：** 编译时加 `-g`（可以和 `-O2` 同时用）。发布时符号常被剥离（strip）到单独的调试信息文件里，要保存好与每个构建一一对应的符号，否则栈里只有 `??` 和地址。

**确认已经打开**：故意让一个进程崩一次：`sleep 100 & kill -SEGV $!`，看转储是否出现在预期位置。

**各语言的差别**：
- **C/C++/Rust：** 就是上面这套。Rust 的 `panic` 默认是有序退出，不产生转储；设 `panic = "abort"` 后才会。
- **Go：** 默认崩溃只打印 goroutine 栈；`GOTRACEBACK=crash` 才会触发 core dump，用 `dlv core ./bin core` 打开。
- **Java：** JVM 崩溃时写 `hs_err_pid<PID>.log`（包含崩溃时的原生栈和寄存器），同时按系统设置生成 core。
- **Python：** 纯 Python 异常不会产生转储；原生扩展里的段错误会。`python -X faulthandler`（或 `faulthandler.enable()`）至少能在崩溃时把 Python 层的栈打印到 stderr。

**代价**：转储大小约等于进程的内存占用，几十 GB 的进程会写出几十 GB，要给目录留空间或限制数量。
