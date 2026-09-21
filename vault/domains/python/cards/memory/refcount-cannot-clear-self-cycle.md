---
id: refcount-cannot-clear-self-cycle
node: memory.refcounting
type: qa
source: cpython-internals
---
## Q
执行 `container = []; container.append(container); del container` 之后，`container` 之前指向的那个列表对象为什么不会被立即释放？

## A
该列表把自己放进了自己内部，形成一条指向自身的内部引用；`del container` 只删掉了外部变量这一条引用，列表内部那条自引用仍在，引用计数（reference count）永远降不到 0。单靠引用计数机制无法清理这种环，必须由专门的循环垃圾回收器扫描不可达的引用环才能回收它。
