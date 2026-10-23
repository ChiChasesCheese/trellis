---
id: hl-cq-q25-errors-include-const
node: cpp-questions.f-ub-debug
type: qa
step: 12
---
## Q
两个常见编译错误怎么认、怎么修：（1）忘了 `#include <vector>` 却写了 `std::vector<int> v;`；（2）`'this' argument to member function 'length' has type 'const Book', but function is not marked const`。

## A
- **缺 `#include`**：现象是 `use of undeclared identifier 'std'`、`expected '(' for function-style cast…` 等，**一行代码引出 4 个错误**——一个缺失造成连锁错误。修法：补 `#include`，只修第一个再重编。
- **const 正确性**：在常量引用上调用了非 `const` 成员函数。修法：给只读成员函数加 `const`。
