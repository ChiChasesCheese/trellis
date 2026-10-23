---
id: hl-cq-q08-brace-vs-paren
node: cpp-questions.b-standards
type: qa
step: 10
---
## Q
`std::vector<int> a{3, 4};` 和 `std::vector<int> b(3, 4);` 各得到什么？`const int& rx = x; auto copy = rx;` 里 `copy` 是什么类型？

## A
```cpp
std::vector<int> brace{3, 4};   // 优先 initializer_list：2 个元素 3, 4
std::vector<int> paren(3, 4);   // 圆括号：3 个元素，每个都是 4
int x = 1;  const int& rx = x;
auto copy = rx;                 // auto 丢掉 const 和引用 -> 普通 int 拷贝
```
- 实测：`vector<int>{3,4}` 有 2 个元素，`vector<int>(3,4)` 有 3 个。
- `copy` 是一个普通 `int` 拷贝，改它不影响原值（改成 2 后原值仍是 1）。想保留引用要写 `const auto&`。
