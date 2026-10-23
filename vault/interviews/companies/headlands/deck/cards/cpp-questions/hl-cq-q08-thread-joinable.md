---
id: hl-cq-q08-thread-joinable
node: cpp-questions.b-standards
type: qa
step: 13
---
## Q
`std::thread` 对象在仍然 joinable（既没 `join` 也没 `detach`）时被析构，会发生什么？C++20 的哪个类型解决了这个问题？

## A
- 析构时会调用 `std::terminate`，程序直接终止。
- C++20 的 **`std::jthread`** 在析构时自动 `join`，所以不会出现这个问题。
