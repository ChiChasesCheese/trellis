---
id: hl-javaq-c-q07-follow-ups
node: java-questions.c-languages
type: qa
step: 4
---
## Q
追问：GIL（全局解释器锁）到底保护什么？Java 怎么向方法传对象？
What exactly does the GIL protect? How does Java pass objects to methods?

## A
- **GIL 保护的是解释器内部状态**，主要是引用计数；**不是你的数据**，所以多线程改共享数据仍然要加锁。它使同一时刻只有一个线程执行 Python 字节码，所以 CPU 密集任务要用多进程或原生扩展。
- **Java 传对象**：引用按值传递——复制的是引用本身；被调方法可以修改对象内容，但重新赋值形参不会影响调用者的变量。
