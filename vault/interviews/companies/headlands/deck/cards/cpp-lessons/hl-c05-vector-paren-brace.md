---
id: hl-c05-vector-paren-brace
node: cpp-lessons.c05-stl-containers
type: qa
step: 21
---
## Q
`std::vector<int> v(5);` 和 `std::vector<int> v{5};` 有什么区别？

## A
- **圆括号** `v(5)`：5 个元素，每个值初始化为 0。
- **花括号** `v{5}`：初始化列表，**1 个**元素，值为 5。
- 想要 n 个元素用圆括号，想给定具体值才用花括号。
