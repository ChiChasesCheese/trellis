---
id: hl-os-syscall-flow
node: foundations.os-processes-threads-ipc
type: qa
step: 12
---
## Q
系统调用（system call）是什么？一次 `FileChannel.read` 从用户态到内核再回来经过哪些步骤？

## A
用户程序不能直接操作硬件或别的进程的内存。CPU 有**用户态**（受限）和**内核态**（什么都能干）两种特权级。读文件、发网络包、分配大块内存、创建线程都必须请求内核代劳，这个请求就是系统调用。

步骤：
1. Java 代码调用 `FileChannel.read`，经 JNI / JVM 内部到 libc 的 `read(fd, …)`；
2. 执行 syscall 指令（x86-64：`syscall`；ARM64：`svc`）陷入内核；
3. 内核保存用户寄存器、切到内核栈，查系统调用表到 `sys_read`，检查参数和权限，真正干活；
4. 恢复用户寄存器，返回用户态，拿到返回值继续执行。
