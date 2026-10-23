---
id: hl-cq-q41-param-passing
node: cpp-questions.j-cross-language
type: qa
step: 10
---
## Q
C++ 函数参数：按值、`T&`、`const T&`、指针各有什么效果？大对象只读、要修改、“可能没有”分别用哪种？`vector` 的拷贝是深拷贝还是浅拷贝？

## A
- **按值**：改的是副本，原对象不变，还多一次拷贝（实测 `copies +1`，原对象 `a.qty` 保持 7）。
- **`T&`**：可通过它修改原对象（`a.qty=-2`）。
- **`const T&`**：只读，不拷贝。
- **指针**：可修改原对象（`a.qty=-3`），也可以表示“可能没有”。
- 选择：大对象只读用 `const T&`；修改用 `T&`；“可能没有”用指针或 `optional`。
- `vector` 的拷贝是**深拷贝**（`v1[0].qty=-3`，`v2[0].qty=999` 互不影响）。
