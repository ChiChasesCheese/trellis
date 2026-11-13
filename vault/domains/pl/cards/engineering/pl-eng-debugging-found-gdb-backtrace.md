---
id: pl-eng-debugging-found-gdb-backtrace
node: engineering.debugging
type: qa
step: 12
---
## Q
拿到了一个核心转储文件和对应的可执行文件。用 gdb 打开后，哪几条命令能最快回答「在哪崩的、当时其他线程在干什么、关键变量是什么值」？

## A
**先看崩溃线程的栈，再看所有线程的栈，最后进入关键的栈帧（frame）看变量。**

```text
$ gdb ./server core.server.4242
(gdb) bt                         # 崩溃线程的调用栈，#0 是崩溃点
#0  Batcher::push (this=0x0, req=...) at batcher.cc:88
#1  Server::handle (...) at server.cc:142
(gdb) frame 1                    # 切到第 1 帧
(gdb) info locals                # 这一帧的局部变量
(gdb) p batcher_                 # 打印表达式：这里是空指针
$1 = (Batcher *) 0x0
(gdb) info threads               # 列出所有线程，* 标出当前线程
(gdb) thread apply all bt        # 每个线程的栈（崩溃常是别的线程造成的）
```

- **`bt full`：** 栈的同时打印每一帧的局部变量，一次看全，适合存档。
- **`thread apply all bt`：** 段错误发生在 A 线程，原因常在 B 线程：B 已经释放了 A 正在用的对象。看所有线程在做什么，是定位「释放后使用」和竞争的关键。
- **批量模式：** `gdb -batch -ex 'bt' -ex 'thread apply all bt' ./server core > crash.txt`，不进交互界面直接导出，适合在 CI 里对每个崩溃自动生成报告并附到测试结果上。
- **读不懂的栈：** 只有 `??` 和地址，说明缺调试符号或符号与二进制版本不匹配；栈很浅、地址很乱，说明栈本身被写坏了，换用 AddressSanitizer 构建复现。
- **优化过的代码：** 变量显示 `<optimized out>` 是正常的，`-O2` 下它已不在内存里；需要细看时用 `-O0 -g` 的构建复现。
- **Python 进程：** 装了 Python 的 gdb 扩展后，`py-bt` 打印 Python 层的调用栈，`py-locals` 看 Python 变量，能同时看到「哪段 Python 代码调进了哪个崩溃的 C 函数」。
- **其他语言：** Rust 用 `rust-gdb` 或 `rust-lldb` 读得更清楚；Go 用 `dlv core`；macOS 上对应的是 `lldb`，命令是 `bt`、`thread backtrace all`、`frame variable`。
