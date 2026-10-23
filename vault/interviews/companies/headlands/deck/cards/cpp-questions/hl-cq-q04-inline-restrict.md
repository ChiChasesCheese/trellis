---
id: hl-cq-q04-inline-restrict
node: cpp-questions.a-why-fast
type: qa
step: 23
---
## Q
追问：`inline` 关键字今天起什么作用？`restrict`（`__restrict`）又是什么？
What does `inline` do? What is `restrict`?

## A
- **`inline`**：历史上是内联的提示；今天主要是允许多个相同定义存在，是否内联由编译器自己决定。
- **`restrict` / `__restrict`**：向编译器承诺“这些指针不别名”，让它能更激进地向量化。它不是标准 C++，但主流编译器都支持。
