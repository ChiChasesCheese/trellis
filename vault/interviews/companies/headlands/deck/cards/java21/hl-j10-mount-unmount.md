---
id: hl-j10-mount-unmount
node: java21.j10-virtual-threads
type: qa
step: 12
---
## Q
一个虚拟线程调用 `Thread.sleep(100)` 时，从被挂载（mount）到再次被挂载，发生了哪几步？

## A
1. 调度器把虚拟线程 `V` **挂载**到空闲载体：把堆上保存的栈帧按需拷回载体的栈，接着跑。
2. `V` 执行 `sleep`：JDK 里的阻塞实现被改写过，不让 OS 线程睡，而是调 `LockSupport.park`，park 在虚拟线程上变成 **yield**：栈帧拷出存进堆（`StackChunk` 对象），`V` 被**卸载**（unmount），载体立刻去跑别的虚拟线程。
3. 定时器到点（或 socket 可读）时，JDK 内部调用 `unpark(V)`，把 `V` 重新提交给调度器。
4. 某载体空了再挂载，从 `sleep` 返回处继续。

写代码的人**看不见**这一切：调用栈、局部变量、异常都保持不变。
