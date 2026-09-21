---
id: refcount-inc-dec-triggers
node: memory.refcounting
type: cloze
source: cpython-internals
---
CPython 对象头部的引用计数（reference count，`ob_refcnt`）在 {{c1::新增一处引用（赋值、传参、放入容器等）}} 时加一，在 {{c2::一处引用消失（变量被覆盖、`del`、作用域退出、从容器移除等）}} 时减一，减到 0 时对象立即释放。
