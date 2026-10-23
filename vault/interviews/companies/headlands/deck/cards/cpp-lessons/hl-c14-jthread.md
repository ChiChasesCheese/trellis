---
id: hl-c14-jthread
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 12
---
## Q
C++20 的 `std::jthread` 和 `std::stop_token` 是什么？比 `std::thread` 好在哪？写出协作式取消的 worker。

## A
- `jthread`：析构时自动 `request_stop()` 再 `join()`，**不会 `terminate`**。
- `stop_token`：线程函数的第一个参数；循环里检查 `stop_requested()`。协作式：线程自己检查，没人强杀。

```cpp
void worker(std::stop_token st, std::atomic<int>& ticks) {
    while (!st.stop_requested()) {
        ++ticks;
        std::this_thread::sleep_for(1ms);
    }
}
```
- 对比 Java 的 `Thread.interrupt()`。
