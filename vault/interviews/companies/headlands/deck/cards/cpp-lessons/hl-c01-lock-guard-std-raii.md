---
id: hl-c01-lock-guard-std-raii
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 10
---
## Q
C++ 里相当于 Java `synchronized (m) { ... }` 的写法是什么？标准库里有哪些常见的 RAII 类型？

## A
```cpp
std::mutex m;
void locked_increment() {
    std::lock_guard<std::mutex> lock(m);   // 构造时加锁，析构时解锁
    ++counter;
    if (counter > 100) throw std::runtime_error("too big");  // 锁仍会释放
}
```
`lock_guard` 就是 `synchronized` 的 RAII 版：无论正常返回还是抛异常，离开作用域都会解锁。

标准库里的 RAII 类型：
- `vector` / `string`：内存
- `unique_ptr` / `shared_ptr`：对象
- `lock_guard` / `unique_lock` / `scoped_lock`：锁
- `fstream`：文件
- `jthread`：线程
