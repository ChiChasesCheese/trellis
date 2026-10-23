---
id: hl-cq-q22-crtp
node: cpp-questions.e-templates
type: qa
step: 13
---
## Q
补全 CRTP：基类模板 `Base<D>` 的 `run()` 调用派生类的 `step()` 再加 1；`Impl` 如何继承？CRTP 的好处和代价各是什么？

## A
```cpp
template <class D> struct Base { int run() { return static_cast<D*>(this)->step() + 1; } };
struct Impl : Base<Impl> { int step() { return 41; } };   // CRTP
```
- 派生类把自己作为模板参数传给基类，基类通过 `static_cast<D*>(this)` 调用它。
- 好处：**编译期绑定、可内联、没有 vptr**。
- 代价：失去运行时多态——不同派生类是互不相关的类型，不能放进同一个容器。
