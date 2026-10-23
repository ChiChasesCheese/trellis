---
id: hl-c07-specialization
node: cpp-lessons.c07-templates-constexpr-concepts
type: qa
step: 6
---
## Q
模板的全特化和偏特化分别是什么？函数模板能偏特化吗？

## A
```cpp
template <typename T> struct Name { static const char* get() { return "other"; } };
template <> struct Name<int> { static const char* get() { return "int"; } };                  // 全特化
template <typename T> struct Name<T*> { static const char* get() { return "pointer"; } };     // 偏特化
```
- **全特化**：针对某个具体类型（`Name<int>`）。
- **偏特化**：针对一类类型（所有指针 `Name<T*>`）。
- **函数模板不支持偏特化**，用重载或 `if constexpr` 代替。
