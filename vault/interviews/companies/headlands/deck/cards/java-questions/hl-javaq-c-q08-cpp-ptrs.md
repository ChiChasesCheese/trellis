---
id: hl-javaq-c-q08-cpp-ptrs
node: java-questions.c-languages
type: qa
step: 6
---
## Q
C++ 的 `unique_ptr`、`shared_ptr`、`weak_ptr` 和 RAII 各自解决什么问题？为什么 C++ 需要它们？

## A
C++ 需要它们，是因为内存和资源的生命周期要由程序员和类型系统精确管理：
- `unique_ptr<T>`：**唯一所有者**，离开作用域就 delete。
- `shared_ptr<T>`：**引用计数**，最后一个释放时 delete；循环引用会让计数永不为 0，造成**泄漏**。
- `weak_ptr<T>`：不增加计数，用来打破循环，使用时 `lock()` 升级为 `shared_ptr`。
- **RAII**（资源获取即初始化）：资源 = 对象生命周期，构造时获取、析构时释放（文件、锁、socket）。
