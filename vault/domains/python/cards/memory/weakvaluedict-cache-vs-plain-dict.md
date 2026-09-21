---
id: weakvaluedict-cache-vs-plain-dict
node: memory.weakref
type: qa
source: python-docs
---
## Q
用普通 `dict` 缓存大对象（如按名字缓存大图片对象）和用 `weakref.WeakValueDictionary` 缓存，最大的区别是什么？

## A
普通 dict 会对存进去的 value 持有一份强引用，只要缓存条目还在，对象就不会被回收，哪怕代码里别处早已不再需要它，缓存本身反而变成了「意外的常驻内存」；`WeakValueDictionary` 只对 value 持弱引用，一旦对象在别处的最后一份强引用消失，垃圾回收器可以立即回收它，对应的缓存条目也会被自动删除，缓存不会仅仅因为「对象出现在缓存里」而把对象的生命周期强行拉长。
