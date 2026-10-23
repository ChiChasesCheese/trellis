---
id: hl-cq-q41-dangling
node: cpp-questions.j-cross-language
type: qa
step: 12
---
## Q
悬空引用在 C++ 里有哪几种常见来源？编译器和运行时工具能抓住哪些？

## A
- 常见成因：返回局部变量的引用（例如 `longest()` 里 `return tmp;`）；被失效的 `vector` 迭代器；比所有者活得久的视图（如 `string_view`）。
- 抓法：简单情形编译器会警告（`-Wreturn-stack-address`）；运行时 ASan 的 `detect_stack_use_after_return` 也能抓到，其余靠 ASan。
