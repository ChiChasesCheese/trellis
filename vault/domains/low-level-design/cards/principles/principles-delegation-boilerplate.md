---
id: principles-delegation-boilerplate
node: principles.composition
type: qa
---
## Q
什么时候你会看到委托而不是继承，什么时候 Extract Class 会引入样板代码？

## A
当 A 委托给 B 时——B 的公共接口完全被 A "代理" 到那些委托方法中。这不是组合，而是代理对象，通常是因为继承会带来不必要的复杂性或紧耦合。

Extract Class 可能会导致样板代码，当：
- 新类只是持有从原始类转移的字段，但没有实现新的行为
- 原始类需要获取器和设置器来访问新类的字段
