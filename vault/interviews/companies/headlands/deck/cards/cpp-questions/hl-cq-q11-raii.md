---
id: hl-cq-q11-raii
node: cpp-questions.c-memory-ownership
type: qa
step: 1
---
## Q
面试题：什么是 RAII？它怎么取代 `finally` / try-with-resources？对象分别住在栈、堆、静态区哪里？
What is RAII, and how does it replace `finally` / try-with-resources? Where do objects live: stack, heap, static?

## A
- **RAII**（Resource Acquisition Is Initialization）：构造函数获取资源，析构函数释放资源。
- 对象离开作用域时（正常返回或异常展开），析构函数**一定**按构造的**逆序**运行，所以文件、锁、内存都不需要 `finally`。
- 对比 Java 的 try-with-resources：C++ 是自动的、由类型保证，不靠调用者自觉。
- 存储位置：栈对象离开作用域自动销毁；堆对象要配对释放或交给智能指针；全局 / `static` 对象在程序开始时构造、结束时销毁。
