---
id: hl-c06-mutable-initcapture
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 11
---
## Q
lambda 的 `mutable` 关键字和初始化捕获（init-capture，`[p = std::move(owned)]`）分别解决什么问题？

## A
- 按值捕获的变量在 lambda 里默认是 `const`。`mutable` 允许修改 **lambda 自己的副本**，外部变量不变。

```cpp
int counter = 0;
auto inc = [counter]() mutable { return ++counter; };
inc(); inc();   // 外面的 counter 仍是 0，lambda 内的副本到 3
```
- **初始化捕获（C++14）**：把 move-only 对象（如 `unique_ptr`）放进 lambda 的**唯一办法**：

```cpp
auto owned = std::make_unique<int>(5);
auto taker = [p = std::move(owned)] { return *p * 2; };  // 10，owned 变空
```
