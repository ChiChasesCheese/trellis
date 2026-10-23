---
id: hl-c14-thread-args
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 3
---
## Q
`std::thread t(add_to, total, 5);`（`add_to` 的第一个参数是 `int&`）为什么编译不过？怎么写？忘记 `join` 会怎样？

## A
```cpp
int total = 0;
std::thread t1(add_to, std::ref(total), 5);   // std::ref 请求引用
t1.join();                                    // total == 5
```
- 参数默认被**拷贝**进线程，拷贝不能绑定到 `int&`；要引用必须 `std::ref`。lambda 的 `[&]` 要保证被引用对象比线程活得久。
- `std::thread` 析构时若没有 `join()`/`detach()`，直接 `std::terminate`。
- `detach` 后线程无人管理，极易访问已销毁的数据，**避免**。
