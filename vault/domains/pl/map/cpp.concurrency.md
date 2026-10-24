%% trellis:begin %%
# 并发：线程、原子与内存序、协程
*现代 C++：特性、取舍与最佳实践*

std::thread 与 jthread、mutex 与 scoped_lock、std::atomic 与六种 memory_order、C++20 协程是无栈协程且需要库支持、与 Rust/Go/Java 模型的对照。

**Requires:** [[domains/pl/map/concurrency.atomics-memory-models|原子操作与内存模型]], [[domains/pl/map/cpp.raii-ownership|RAII、零/三/五法则与智能指针]]

## Cards (11)
1. [[pl-cpp-concurrency-principle]]
2. [[pl-cpp-concurrency-found-thread-jthread]]
3. [[pl-cpp-concurrency-found-mutex-scoped-lock]]
4. [[pl-cpp-concurrency-found-atomics-race]]
5. [[pl-cpp-concurrency-found-memory-order]]
6. [[pl-cpp-concurrency-found-coroutines]]
7. [[pl-cpp-concurrency-mechanism-costs]]
8. [[pl-cpp-concurrency-table]]
9. [[pl-cpp-concurrency-unique-mechanism-not-policy]]
10. [[pl-cpp-concurrency-best-practice]]
11. [[pl-cpp-concurrency-pitfall-invisible-race]]
%% trellis:end %%

## Notes
