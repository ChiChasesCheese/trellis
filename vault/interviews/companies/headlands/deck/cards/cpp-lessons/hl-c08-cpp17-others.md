---
id: hl-c08-cpp17-others
node: cpp-lessons.c08-cxx-standards-tour
type: qa
step: 9
---
## Q
除了 `optional`/`variant`/结构化绑定，C++17 还加了哪些语言和库特性？各自为什么加？

## A
- **`if constexpr`**、折叠表达式、**CTAD**（类模板参数推导，`std::pair p(1, 2.5)`）：取代 SFINAE；简化可变参数；少写模板参数。
- **保证的复制省略**：用纯右值初始化对象不产生临时对象，可返回不可拷贝类型。
- `inline` 变量、嵌套命名空间 `a::b::c`：头文件里定义常量；少缩进。
- `[[nodiscard]]`、`[[maybe_unused]]`、`[[fallthrough]]`：编译器帮忙检查。
- 库：`std::filesystem`、并行算法（`std::reduce`、`execution::par`）、`from_chars/to_chars`、`gcd/lcm/clamp`、`try_emplace/insert_or_assign`。
