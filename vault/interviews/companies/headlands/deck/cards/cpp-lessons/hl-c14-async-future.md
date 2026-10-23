---
id: hl-c14-async-future
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 4
---
## Q
面试问：`std::async` 和 `std::thread` 的区别？线程里抛的异常怎么传回来？
Interview question: What is the difference between `std::async` and `std::thread`?

## A
- `std::async` 返回 `future`，能传回**结果和异常**；`get()` 等待并**重新抛出**任务里的异常。
- 直接从 `std::thread` 的函数里逃出的异常会 `std::terminate`。
- `async` 默认策略可能**延迟执行**，用 `std::launch::async` 强制新线程；来自 `async` 的 `future` 析构会阻塞等待。

```cpp
auto left = std::async(std::launch::async, [&] {
    return std::accumulate(v.begin(), mid, 0L);
});
long right = std::accumulate(mid, v.end(), 0L);
return left.get() + right;
```
