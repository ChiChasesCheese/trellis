---
id: hl-cq-q41-slicing
node: cpp-questions.j-cross-language
type: qa
step: 11
---
## Q
`Animal sliced = d;`（`d` 是 `Dog`）和 `Animal& ref = d;` 调用 `name()` 各得到什么？`vector<Animal>` 里放 `Dog` 呢？多态对象应该怎么存？

## A
- `Animal sliced = d;` 只拷贝基类子对象：`name()` 得到 `"animal"`。
- `Animal& ref = d;` 保持多态：`name()` 得到 `"dog"`。
- `vector<Animal>` 里放派生类对象同样被切片，`name()` 是 `"animal"`。
- 多态对象要通过**指针或引用**使用：容器里放 `std::vector<std::unique_ptr<Animal>>`。
