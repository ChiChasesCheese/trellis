---
id: pickle-copyreg-customize-third-party-class
node: engineering.serialization
type: qa
source: python-docs
---
## Q
想让一个自己无法修改源码的第三方类能被 `pickle` 正确序列化/反序列化（或者想改变默认的 pickle 方式），可以用什么机制，而不用去改这个类本身？

## A
`copyreg` 模块维护一张全局「派发表」（dispatch table），把「类」映射到「一个知道如何把该类实例还原成可重建形式的函数」（reduction function）。调用 `copyreg.pickle(SomeClass, reduce_SomeClass)` 就把 `SomeClass` 注册进这张全局表，之后所有对该类实例的 pickle 操作都会改用 `reduce_SomeClass` 来决定怎么序列化，完全不需要修改 `SomeClass` 的源码；也可以只给某个 `Pickler` 实例设置私有的派发表副本，只影响这一个 pickler 而不影响全局。
