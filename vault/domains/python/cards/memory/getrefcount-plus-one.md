---
id: getrefcount-plus-one
node: memory.refcounting
type: qa
source: cpython-internals
---
## Q
为什么 `sys.getrefcount(x)` 返回的值，总比 x 实际被引用的次数多 1？

## A
因为调用 `sys.getrefcount(x)` 时，x 作为参数被传给这个函数，函数体内临时持有一份指向 x 的引用；这份临时引用在函数返回前还没释放，所以返回值 = 实际引用计数（reference count）+ 这一次调用带来的临时引用。
