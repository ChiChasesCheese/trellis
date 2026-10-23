---
id: hl-cq-cs12-vector
node: cpp-questions.cheatsheet
type: qa
step: 12
---
## Q
一句话背诵：`std::vector` 的扩容序列、失效规则和 `reserve` 的效果。

## A
- 翻倍扩容：`1 2 4 … 128`。
- 扩容使**所有**迭代器、指针、引用失效。
- `erase` 使被删位置及之后的失效。
- 先 `reserve`：1000 次 `push_back` 从 **11 次**分配降到 **1 次**。
