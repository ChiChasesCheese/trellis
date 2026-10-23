---
id: hl-c06-generic-recursive-lambda
node: cpp-lessons.c06-algorithms-lambdas-ranges
type: qa
step: 12
---
## Q
什么是泛型 lambda？怎样写不借助 `std::function` 的递归 lambda？什么是立即调用的 lambda（IIFE）？

## A
- **泛型 lambda（C++14）**：参数写 `auto`，编译器生成模板化的 `operator()`：`[](auto a, auto b) { return a + b; }` 可用于 `int`、`double`、`string`。
- **递归 lambda**：把自己作为参数传入，避免 `std::function`：

```cpp
auto fact = [](auto&& self, int n) -> long {
    return n <= 1 ? 1 : n * self(self, n - 1);
};
fact(fact, 10);   // 3628800
```
- **IIFE**：创建后立即调用，用逻辑初始化一个 `const`：`const int v = [] { return 6 * 7; }();`
