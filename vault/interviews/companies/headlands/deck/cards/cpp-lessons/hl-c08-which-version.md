---
id: hl-c08-which-version
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 15
---
## Q
自测：`make_unique`、`optional`、`<=>`、`unique_ptr`、`if constexpr`、`jthread` 分别是哪个 C++ 版本引入的？

## A
- `make_unique`：**C++14**（C++11 只有 `make_shared`）
- `optional`：**C++17**
- `<=>`：**C++20**
- `unique_ptr`：**C++11**
- `if constexpr`：**C++17**
- `jthread`：**C++20**

常见错误：把 `make_unique` 说成 11；把 `optional/variant/string_view/结构化绑定` 说成 20（都是 17）；把 ranges、`std::format` 说成 17（都是 20）。
