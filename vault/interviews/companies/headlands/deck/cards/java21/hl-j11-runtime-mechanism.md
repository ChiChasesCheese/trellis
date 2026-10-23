---
id: hl-j11-runtime-mechanism
node: java21.j11-structured-concurrency
type: qa
step: 10
---
## Q
运行时 `StructuredTaskScope` 靠哪些机制实现「结构化」？取消是怎么做的？

## A
1. **线程容器**（thread container）：每个 scope 内部记录它 fork 出的所有线程，`close()` 就是等容器里的线程全终止。
2. **父子关系可见**：线程 dump（`jcmd <pid> Thread.dump_to_file -format=json`）显示线程属于哪个作用域，名字即构造器第一个参数。
3. **取消 = 中断**：`shutdown()` 对每个存活子线程 `interrupt()`，是**协作式**的，子任务要在阻塞调用（`sleep`、`take`、socket 读）上响应中断，或自己轮询 `Thread.interrupted()`；纯 CPU 循环取消不掉。
4. **作用域值继承**：子线程自动继承父线程当前的 `ScopedValue` 绑定。
5. **嵌套被检查**：JVM 记录线程上当前打开的作用域栈，关闭顺序不对抛 `StructureViolationException`。
