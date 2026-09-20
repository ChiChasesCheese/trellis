---
id: patterns-flyweight-when
node: patterns.structural
type: qa
step: 7
---
## Q
什么时候 Flyweight 值得引入？它的成本和收益分别是什么？

## A
当你有**大量相似对象**、内存是瓶颈时才值得。Flyweight 把**共享的、不可变的**状态（intrinsic，比如字符字形）和**每个对象独有的、可变的**状态（extrinsic，比如它在文档里的位置）拆开——intrinsic 部分只存一份，用一个按 key 缓存的工厂函数（常常就是 `functools.lru_cache` 包起来的构造函数）复用它。

成本：多了两套状态要分别管理，多了一次查缓存的开销（比直接构造慢，但比重复构造省内存）。经验法则：对象数量上万、且共享比例超过八成时才考虑；对象数量小或者大多互不相同时，Flyweight 增加的复杂度换不回内存收益。
