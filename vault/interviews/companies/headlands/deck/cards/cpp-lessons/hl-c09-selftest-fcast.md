---
id: hl-c09-selftest-fcast
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 17
---
## Q
自测：`float f; int i = *(int*)&f;` 违反了什么规则？写出合法的两种写法。

## A
- 违反**严格别名**（strict aliasing）规则，UB。
- 合法写法：`std::memcpy(&i, &f, sizeof i);`，或 C++20 的 `i = std::bit_cast<int>(f);`。
