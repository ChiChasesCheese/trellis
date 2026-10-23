---
id: hl-c08-cpp11-concurrency
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 4
---
## Q
C++11 的并发库包含什么？为什么它是里程碑？写出 4 线程各累加 1000 次的 `atomic` + `mutex` 例子。

## A
- 包含：`thread`、`mutex`、`atomic`、`condition_variable`、`future`，以及**内存模型**。
- 里程碑：语言**第一次定义多线程语义**；之前只能用平台 API（pthread、Win32）。

```cpp
std::atomic<int> hits(0);
std::mutex mu;
int guarded = 0;
std::vector<std::thread> ts;
for (int i = 0; i < 4; ++i)
    ts.push_back(std::thread([&] {
        for (int j = 0; j < 1000; ++j) {
            ++hits;
            std::lock_guard<std::mutex> g(mu); ++guarded;
        }
    }));
for (auto& t : ts) t.join();   // hits == 4000, guarded == 4000
```
