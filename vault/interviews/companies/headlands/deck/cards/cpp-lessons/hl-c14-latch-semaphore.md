---
id: hl-c14-latch-semaphore
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 14
---
## Q
C++20 的 `std::latch`、`std::barrier`、`std::counting_semaphore` 分别是什么？限制同时进入临界段的线程数怎么写？

## A
- `std::latch`：**一次性**倒计数，`count_down()` 归零后 `wait()` 放行。
- `std::barrier`：**可重复**使用的同步点。
- `std::counting_semaphore<N>`：计数信号量，限制并发数。

```cpp
std::latch ready(3);
std::counting_semaphore<2> slots(2);     // 同时最多 2 个
// 每个 jthread：
slots.acquire();
/* 临界段 */
slots.release();
ready.count_down();
// 主线程：ready.wait();
```
- 实测：3 个 worker 中同时在临界段内最多 2 个（上限 2）。
