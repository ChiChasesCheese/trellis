---
id: hl-cq-q40-java-vs-cpp
node: cpp-questions.j-cross-language
type: qa
step: 1
---
## Q
面试题：你每天用 Java，Java 和 C++ 的主要区别是什么？
You use Java every day. What are the main differences between Java and C++?

## A
核心一句话：**Java 替你管内存和安全，C++ 把控制权和责任都交给你。**
- **Java**：对象在堆上、变量是引用、GC 回收、泛型擦除、数据竞争有定义。
- **C++**：对象是**值**（可在栈上或内联在别的对象里）、手动 / RAII 管理生命周期、模板实例化、很多错误是未定义行为，编译模型是头文件 + 链接。
