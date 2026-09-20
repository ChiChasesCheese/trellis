---
id: problems-pub-sub-no-new-singleton
node: problems.components.pub-sub
type: qa
step: 10
tags: [grown]
---
## Q
流传最广的 Pub-Sub 参考实现把总线写成 `__new__` 单例（`PubSubService._instance` 加双重检查锁）。在 Python 里这有什么问题？替代写法是什么？

## A
它把『全局只要一个』和『这个类本身』焊死了：测试再也拿不到干净的实例，两个用例之间主题表互相污染，想在一个进程里跑两套隔离的总线（插件、多租户）也做不到。双重检查锁还额外带来一个 `_initialized` 标志的坑——`__init__` 每次构造都会被调用。

Python 的单例是**模块级的一个对象**：总线写成普通类 `Broker()`，需要全局默认实例就在模块底部放一个、或者用一个 `default_broker()` 惰性函数。需要隔离的场合各 `Broker()` 一个就是了。同一条判断也适用于日志框架的 manager、限流器的注册表：`__new__` 单例在 Python 里几乎永远是 Java 习惯的转写。
