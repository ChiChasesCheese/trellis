---
id: cbr-role-debug-tools
node: role.tools
type: qa
step: 2
---
## Q
一个推理测试进程卡住或崩溃了，用哪些 Linux 和 Python 工具排查？每个看什么？

## A
| 工具 | 命令 | 看什么 |
|---|---|---|
| `top` / `htop` | `top -p <pid>` | CPU 是满的（死循环、在算）还是 0（在等） |
| `strace` | `strace -f -p <pid>` | 进程在做哪个系统调用：卡在 `read`、`futex`（等锁）还是网络 |
| `py-spy` | `py-spy dump --pid <pid>` | 每个 Python 线程当前的调用栈，不用停进程 |
| `gdb` | `gdb -p <pid>` 后 `thread apply all bt` | C/C++ 层每个线程的栈，看死锁 |
| `pdb` | `python -m pdb` 或 `breakpoint()` | 单步调试 Python |
| 日志 | 按请求 ID 串起来 | 跨组件的时间线：哪一层最后一次正常 |

- **顺序**：先看现象（CPU、内存）→ 再看在等什么（系统调用、锁）→ 再看代码在哪（栈）→ 最后按请求 ID 拼出跨层时间线。
- **你的诚实线**：可观测性（Sentry、Datadog、交易追踪）是你的强项；`gdb`、`strace` 是在学的一层。
