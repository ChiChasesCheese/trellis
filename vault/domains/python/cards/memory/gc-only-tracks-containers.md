---
id: gc-only-tracks-containers
node: memory.cyclic-gc
type: qa
source: cpython-internals
---
## Q
`gc` 模块的循环垃圾回收器（cyclic garbage collector）只追踪（track）哪一类对象？为什么 `int`、`str` 这类对象不需要被它追踪？

## A
只追踪能够持有其他对象引用的「容器对象」（container objects，如 list、dict、自定义类实例）。`int`、`str` 这类原子（atomic）对象不可能引用别的对象，不可能参与引用环，所以从创建起就不被 GC 追踪；`gc.is_tracked(0)` 和 `gc.is_tracked("a")` 都是 `False`，而 `gc.is_tracked([])` 是 `True`。
