---
id: weakref-proxy-vs-ref-failure-mode
node: memory.weakref
type: qa
source: python-docs
---
## Q
`weakref.ref(obj)` 和 `weakref.proxy(obj)` 在「引用的对象已经被回收」之后，各自会有什么不同的失败表现？

## A
`weakref.ref(obj)` 得到的弱引用对象本身还在，调用它（像调用函数一样 `r()`）会返回 `None`，需要调用方自己检查返回值是不是 `None` 才能安全使用；`weakref.proxy(obj)` 得到的是一个「代理」对象，用起来像直接用原对象（不用显式调用），但一旦原对象已被回收，访问代理对象的任何属性都会直接抛出 `ReferenceError`，需要调用方捕获这个异常或提前判断，而不是拿到一个可以安全判空的返回值。
