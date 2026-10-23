---
id: hft-cpp-static-dispatch-crtp
node: cpp.static-dispatch
type: qa
step: 2
---
## Q
CRTP（curiously recurring template pattern，奇异递归模板模式）是怎么在不使用虚函数的前提下实现“基类定义流程、子类提供细节”的？

## A
做法：子类把**自己**当作模板参数传给基类。

- 基类写成 `template <class Derived> struct Strategy`。
- 基类里的 `on_tick()` 想调用子类的细节时，写 `static_cast<Derived*>(this)->on_tick_impl()`。
- 子类写成 `struct MyStrategy : Strategy<MyStrategy>`，并实现 `on_tick_impl()`。

因为 `Derived` 在**编译期**就知道，编译器直接生成对 `MyStrategy::on_tick_impl` 的调用，可以内联，没有虚表指针，也没有间接跳转。

例：一个交易框架把“收到行情 → 调策略 → 风控 → 发单”这套固定流程写在基类，不同策略只实现中间的计算；用 CRTP 后，整条热路径可以被编译器作为一个整体优化。

限制：类型必须在编译期确定，不能在运行时用同一个基类指针存放不同的策略对象。
