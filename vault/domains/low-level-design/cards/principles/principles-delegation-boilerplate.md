---
id: principles-delegation-boilerplate
node: principles.composition
type: qa
step: 4
---
## Q
什么时候你会看到委托而不是继承？什么时候"提取一个类"（Extract Class）反而会引入样板代码？

## A
当 `A` 委托给 `B` 时——`B` 的公共接口被 `A` 原样"代理"到一堆转发方法里。这不是真正意义上的组合复用，而是一个包装对象，通常是因为继承在这里会带来不必要的耦合或复杂性。

Extract Class 会变成样板代码，当：
- 新提取出来的类只是把字段从原来的类里搬过去存着，没有实现任何新行为；
- 原来的类因此需要一堆纯转发的方法（`get_x`/`set_x`）去访问新类里的字段，没有增加任何封装收益。
