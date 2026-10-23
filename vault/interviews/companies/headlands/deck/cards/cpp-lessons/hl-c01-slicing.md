---
id: hl-c01-slicing
node: cpp-lessons.c01-value-lifetime-raii
type: qa
step: 12
---
## Q
什么是切片（slicing）？`std::string by_value(Animal a)` 传入 `Dog` 会发生什么？怎么避免？

## A
- 按**值**接收基类参数时，只复制派生类对象里的**基类部分**，派生类的字段（如 `Dog::tricks`）和虚函数覆盖都丢失，多态失效。
- 例：`by_value(Dog{})` 里 `a.name()` 返回 `"animal"`；而 `by_ref(const Animal& a)` 返回 `"dog"`，因为没有复制，虚函数分派正常。
- 避免：多态对象只用**引用或指针**传递（`const Animal&`、`Animal*`、`unique_ptr<Animal>`），基类析构函数写成 `virtual`。
