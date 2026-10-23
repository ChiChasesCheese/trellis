---
id: hl-cq-q03-internal-linkage
node: cpp-questions.a-why-fast
type: qa
step: 17
---
## Q
追问：C++ 在命名空间作用域给函数或变量加 `static` 有什么作用？匿名命名空间是什么关系？
What does `static` at namespace scope do?

## A
- 给这个名字**内部链接**（internal linkage）：每个翻译单元有自己私有的一份，链接器看不到，也不会和别的 `.cpp` 重名冲突。
- **匿名命名空间**（anonymous namespace）是它的现代写法，效果相同。
