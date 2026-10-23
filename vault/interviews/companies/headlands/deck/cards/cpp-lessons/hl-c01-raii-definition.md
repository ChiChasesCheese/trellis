---
id: hl-c01-raii-definition
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 7
---
## Q
什么是 RAII（Resource Acquisition Is Initialization）？为什么 C++ 没有 `finally`？

## A
- **思想**：把资源的所有权绑到一个对象的生命周期上——**构造函数获取资源，析构函数释放**。
- 析构函数在**所有退出路径**（`return`、`break`、异常）上都会被调用，所以不需要 `finally`，也不会漏释放。
- 比 `finally` 好在「写一次，处处生效」，调用者不会忘。
- Java 的 `try-with-resources` 是同一思想的特例，但要调用者记得写；C++ 的 RAII 适用于**一切**资源：内存、文件、锁、socket、事务。
- 口述版："Lifetime is tied to scope; the destructor runs on every exit path, including exceptions. I put every resource - memory, file, lock - in an object, so cleanup is automatic."
