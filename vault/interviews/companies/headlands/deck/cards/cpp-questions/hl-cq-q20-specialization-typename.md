---
id: hl-cq-q20-specialization-typename
node: cpp-questions.e-templates
type: qa
step: 4
---
## Q
三个追问：模板特化是什么？为什么不能把模板定义放进 `.cpp`？`typename` 在什么场合必须写？

## A
- **特化**（specialization）：为特定类型（全特化）或一族类型（偏特化，针对类模板）提供不同实现，例如 `std::hash<Point>`。
- **模板定义不能只放 `.cpp`**：编译器在实例化的地方需要看到函数体；否则要用显式实例化（explicit instantiation）。
- **`typename`**：告诉编译器像 `C::value_type` 这样的**依赖名字**是一个类型。
