---
id: hl-cq-q07-optional-vs-expected
node: cpp-questions.b-standards
type: qa
step: 7
---
## Q
追问：函数返回值“可能没有”时，C++ 里你首先会用什么？还要带上错误原因时呢？
Which would you reach for first for an `Optional` return?

## A
- “可能没有值”：`std::optional`（C++17）。
- 还需要告诉调用者出了什么错：`std::expected`（C++23）。
