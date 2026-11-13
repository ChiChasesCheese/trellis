---
id: subprocess-returncode-signals
node: concurrency.multiprocessing
type: qa
---
## Q
一个被测进程的 `returncode` 是 `-9`，另一个 CI 日志里写着 `exit code 137`，第三个是 `-15`。分别说明了什么？`terminate()` 和 `kill()` 有什么区别？

## A
**在 Python 的 `subprocess` 里，负数退出码 `-N` 表示子进程被信号 N 杀死；在 shell 和大多数 CI 里，同样的事情显示为 `128 + N`。所以 `-9` 和 `137` 是同一件事：被 `SIGKILL` 杀了。**

| 看到的值 | 含义 | 常见原因 |
|---|---|---|
| `0` | 正常退出 | — |
| `1`、`2` 等正数 | 程序自己 `exit(n)` | 断言失败、参数错误 |
| `-15` / `143` | 收到 `SIGTERM` | 被 `terminate()`、超时清理、容器停止 |
| `-9` / `137` | 收到 `SIGKILL` | 内存超限被 OOM killer 杀、宽限期后强杀 |
| `-11` / `139` | `SIGSEGV` 段错误 | C/C++ 扩展或驱动里的空指针、越界 |
| `-6` / `134` | `SIGABRT` | `abort()`、断言失败、glibc 检测到堆损坏 |

- **实测：** `Popen(["sleep", "30"])` 后 `terminate()` 得到 `-15`，`kill()` 得到 `-9`；`sh -c 'sleep 30 & kill -9 $!; wait $!'` 的退出码是 `137`。
- **`terminate()` 与 `kill()`：** POSIX 上前者发 `SIGTERM`（可捕获，给程序清理的机会），后者发 `SIGKILL`（不可捕获，立即结束）。两者都只发给这一个进程，不包括它的子进程。
- **`SIGINT`：** Ctrl-C 发的信号，在 Python 里变成 `KeyboardInterrupt`。
- **排查方向：** `-9`/`137` 先查内存（`dmesg` 里有没有 OOM killer 的记录，容器里看是否 `OOMKilled`）；`-11`/`-6` 是原生代码崩溃，去拿 core dump 和 `gdb` 回溯；正数退出码去看程序自己的 stderr。
- **测试里要区分：** 「程序报告失败」（正数）和「程序被外力杀死」（信号）是两类问题，分诊时归给不同的人。
