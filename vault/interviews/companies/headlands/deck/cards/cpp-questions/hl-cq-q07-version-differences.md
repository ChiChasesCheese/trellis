---
id: hl-cq-q07-version-differences
node: cpp-questions.b-standards
type: qa
step: 1
---
## Q
面试题：C++11、14、17、20 有哪些区别？
What are the differences between C++11, 14, 17 and 20?

## A
一句话各版本的定位：
- **11**：现代 C++ 的起点——移动语义、`auto`、lambda、智能指针、线程与原子、`constexpr`、range-for。
- **14**：打磨——泛型 lambda、返回类型推导、`make_unique`。
- **17**：补词汇类型和编译期工具——`optional`/`variant`/`string_view`、结构化绑定、`if constexpr`、保证的复制省略。
- **20**：第二次大改——concepts、ranges、coroutines、modules，外加 `span`、`<=>`、`jthread`、`format`。
- **23**：`std::expected`、`std::print`、显式 `this`。
