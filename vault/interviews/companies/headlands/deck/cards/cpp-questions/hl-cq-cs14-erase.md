---
id: hl-cq-cs14-erase
node: cpp-questions.cheatsheet
type: qa
step: 14
---
## Q
一句话背诵：从 C++ 容器里删除元素的四种正确做法。

## A
- `remove_if` 只前移不缩容（`size` 仍是 6），要接 `erase`。
- 循环里 `it = c.erase(it)`。
- C++20 `std::erase_if`。
- 顺序无关用 swap-and-pop。
