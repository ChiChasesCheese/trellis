---
id: hl-cq-q21-collapse-autoref-emplace-caveat
node: cpp-questions.e-templates
type: qa
step: 9
---
## Q
三个追问：什么是引用折叠（reference collapsing）？`auto&&` 能是转发引用吗？`emplace_back` 一定比 `push_back` 好吗？

## A
- **引用折叠**：`& &`、`& &&`、`&& &` 都变成 `&`，只有 `&& &&` 保持 `&&`。
- **`auto&&`** 可以是转发引用，例如在 range-for 或泛型 lambda 里。
- **`emplace_back` 不总是更好**：对平凡类型没有收益，而且可能掩盖隐式转换或 `explicit` 构造函数。
